import numpy as np
import os, sys
from .search import *
from .inverted_matrix import *
from .postings import *
from .helpers import tokenize_and_stem
from collections import defaultdict
from scipy.sparse.linalg import svds

def tfidf_matrix(tf,idf,companies,word_in,k=10):
	index_to_word = tf.keys()
	word_to_index = {index_to_word[i]:i for i in range(len(index_to_word))}
	index_to_companies = companies
	company_to_index = {company_to_index[i]:i for i in range(len(index_to_companies))}
	n_words = len(index_to_word)
	n_comps = len(companies)
	mat = np.zeros((n_words,n_comps))

    for word in tf.keys():
    	for comp, freq in tf[word]:
    		mat[word_to_index[word]][index_to_companies[comp]] = freq * idf[word]

    words_compressed, _, docs_compressed = svds(mat, k=40)
    docs_compressed = docs_compressed.transpose()

    if word_in not in word_to_index: return "Not in vocab."

	sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
	asort = np.argsort(-sims)[:k+1]
	return [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]

