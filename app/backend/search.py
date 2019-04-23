import math
import numpy as np
import json, os
from app import app

def bool_search(query, matrix):
    s = set()
    for i, word in enumerate(query):
        if i == 0:
            if word in matrix.keys():
                # print(matrix[word])
                for z in matrix[word]:
                    company = z[0]
                    s.add(company)
            else:
                return s
        else:
            e = set()
            for z in matrix[word]:
                company = z[0]
                e.add(company)
            s = s.intersection(e)

    return s

def get_idf(inv_idx, n_docs, max_df_ratio=.99, min_df = 4):
    """ Compute term IDF values from the inverted index.
    Words that are too frequent or too infrequent get pruned.

    Hint: Make sure to use log base 2.

    Arguments
    =========

    inv_idx: an inverted index as above

    n_docs: int,
        The number of documents.

    max_df_ratio: float,
        Maximum ratio of documents a term can occur in.
        More frequent words get ignored.

    Returns
    =======

    idf: dict
        For each term, the dict contains the idf value.

    """
    path = os.path.join(app.root_path, "./backend/idf.json")
    if os.path.isfile(path):
        return json.load(open(path))
    else:
        print("IDF Matrix does not exist. Creating...")
        d = {}

        for word in inv_idx.keys():
            if len(inv_idx[word]) / n_docs < max_df_ratio and \
                len(inv_idx[word]) > min_df:
                idf = math.log((n_docs)/(len(inv_idx[word])+1), 2)
                d[word] = idf
        
        json.dump(d, open(path, 'w'))

        return d

    


def compute_doc_norms(index, idf, n_docs, companies):
    """ Precompute the euclidean norm of each document.

    Arguments
    =========

    index: the inverted index as above

    idf: dict,
        Precomputed idf values for the terms.

    n_docs: int,
        The total number of documents.

    Returns
    =======

    norms: np.array, size: n_docs
        norms[i] = the norm of document i.
    """

    norms = np.zeros(n_docs)

    for word in index.keys():
        for i, j in index[word]:
            if word in idf.keys():
                k = companies.index(i)
                norms[k] += (j * idf[word]) ** 2

    return np.sqrt(norms)


def index_search(query, index, idf, doc_norms, companies):
    """ Search the collection of documents for the given query

    Arguments
    =========

    query: string,
        The query we are looking for.

    index: an inverted index as above

    idf: idf values precomputed as above

    doc_norms: document norms as computed above

    tokenizer: a TreebankWordTokenizer

    Returns
    =======

    results, list of tuples (score, doc_id)
        Sorted list of results such that the first element has
        the highest score, and `doc_id` points to the document
        with the highest score.

    Note:

    """

    result = {}

    tokenized_query = query
    seen = []
    for query_word in tokenized_query:
        if query_word in index.keys() and query_word not in seen:
            for existing_doc, freq in index[query_word]:
                existing_docid = companies.index(existing_doc)
                #took out idf[query_word] AND query word norm
                score = tokenized_query.count(query_word) * freq
                if existing_doc not in result.keys():
                    result[existing_docid] = score
                else:
                    result[existing_docid] += score
            seen.append(query_word)

    for doc_id in result.keys():
        result[doc_id] = result[doc_id] / (doc_norms[doc_id])

    results = []

    for doc_id in result.keys():
        results.append((result[doc_id], doc_id))

    results.sort(key=lambda x: (x[0]), reverse=True)

    return results