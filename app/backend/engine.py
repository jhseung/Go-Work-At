import numpy as np
import os, sys
from .search import *
from .inverted_matrix import *
from .postings import *
from .helpers import tokenize_and_stem
from collections import defaultdict

# takes in a sentence, returns a list of stemmed words
def get_input():
    raw_input = input("What qualities? \n")
    return tokenize_and_stem(raw_input)

def get_company_list():
    s = defaultdict(list)
    ranked_postings = ranked_posting_company()
    for posting in ranked_postings:
        s[(posting['company'].lower())].append(posting['link'])

    return s

def fetch_postings(inp):
    # processed_input = get_input()
    print(inp, file=sys.stderr)
    processed_input = tokenize_and_stem(inp)
    input_companies = get_company_list()
    # json.dump(list(input_companies), open("company_list.json", 'w'))
    inverted_matrix = open_inverted_matrix()
    company_num, company_list = get_comp_number()

    idf = compute_idf(inverted_matrix, company_num)

    doc_norms = compute_doc_norms(inverted_matrix, idf, company_num, company_list)
    # print(doc_norms)

    ranked = index_search(processed_input, inverted_matrix, idf, doc_norms, company_list)
    print(ranked, file=sys.stderr)
    # print("Using cosine similarity, recommended companies and score: ")
    for score, company_id in ranked:
        comp = company_list[company_id]
        if comp in input_companies.keys():
            print((comp, ": ", score), file=sys.stderr)
    
    
    return ranked

# if __name__ == '__main__':
#     main()