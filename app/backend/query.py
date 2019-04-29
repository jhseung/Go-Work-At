import numpy as np
import os, sys
from .search import *
from .inverted_matrix import *
from .postings import *
from .helpers import tokenize_and_stem
from collections import defaultdict
from scipy.sparse.linalg import svds
from nltk.stem import PorterStemmer

def tfidf_matrix(tf,idf,companies,word_in,k=3):
	ps = PorterStemmer()
	index_to_word = list(idf.keys())
	for company in companies:
		if ps.stem(company) in index_to_word:
			index_to_word.remove(ps.stem(company))
	word_to_index = {index_to_word[i]:i for i in range(len(index_to_word))}
	index_to_companies = companies
	company_to_index = {index_to_companies[i]:i for i in range(len(index_to_companies))}
	n_words = len(index_to_word)
	n_comps = len(companies)
	mat = np.zeros((n_words,n_comps))
	for word in index_to_word:
		for comp, freq in tf[word]:
			mat[word_to_index[word]][company_to_index[comp]] = freq * idf[word]
	words_compressed, _, docs_compressed = svds(mat, k=int(n_comps/2))
	docs_compressed = docs_compressed.transpose()

	
	sims = []
	for word in word_in:
		if word in word_to_index:
			if sims == []:
				sims = words_compressed.dot(words_compressed[word_to_index[word],:])
			else:
				sims = np.add(sims,words_compressed.dot(words_compressed[word_to_index[word],:]))
	if sims != []:
		asort = np.argsort(-sims)[:k+1]
		return [(index_to_word[i],sims[i]/sims[asort[0]]) for i in asort[1:]]
	else:
		return []