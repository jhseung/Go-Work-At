import re
import csv
import numpy as np
import os, sys, json
from collections import defaultdict
from app import app
from sklearn.feature_extraction.text import CountVectorizer

def get_company_list_reviews():
	path = os.path.join(app.root_path, "./backend/company_reviews")
	files = os.listdir(path)

	companies = []

	for f in files:
		if f.endswith(".csv"): 
			companies.append(f[:f.rfind('_')])

	return companies

# Creates a cooccurence matrix of shape (n_terms, n_terms)
def get_keywords(company_list):
	
	path = os.path.join(app.root_path, "./backend/keywords.json")
	if not os.path.isfile(path):
		r_postings = []
		for input_company in company_list:
			# Convert the given csv name to a...
			csv_name = 'backend/company_reviews/' + input_company + '_reviews.csv'
			# print(csv_name, file=sys.stderr)
			# postings = csv_to_postings(csv_name)
			# print("postings: {}".format(postings), file=sys.stderr)
			filename = os.path.join(app.root_path, csv_name)
			reader = csv.reader(open(filename, newline='', encoding='utf-8'))
			
			row_count = 0
			for row in reader:
				if row_count != 0:
					r_posting = row[7] + ' ' + input_company
					r_postings.append(r_posting)
				row_count += 1

		stopwords = frozenset(['00','000', '10', '100', '1000', '11', '12', '120', '13', '14', '15', '150', '16', '17', '18', '20', '200', '2000', '2010', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '20s', '21', '22', '24', '25', '250', '2x', '30', '300', '35', '360', '40', '400', '401', '45', '4th', '50', '500', '5pm', '60', '6pm', '70', '80', '90', '95', '9am'])
		c_vec = CountVectorizer(stop_words=stopwords, max_df=0.85, min_df=5, binary = False)

		term_doc_matrix = c_vec.fit_transform(r_postings)
		# term_doc_matrix = np.array(term_doc_matrix)
		features = c_vec.get_feature_names()

		# print(term_doc_matrix.shape, file=sys.stderr)
		cooccurence_matrix = np.dot(term_doc_matrix.T, term_doc_matrix)
		# print(cooccurence_matrix.shape)

		pa = np.reshape(np.sum(term_doc_matrix,0), (term_doc_matrix.shape[1],1))
		# print(pa.shape)
		for i in range(cooccurence_matrix.shape[0]):
			cooccurence_matrix[i,i] = 0
		PMI_part = cooccurence_matrix / pa

		PMI = PMI_part.T / pa

		# print(PMI)

		d = defaultdict(list)
		for company in company_list:
			if company in features:
				idx = features.index(company)
				# print(idx)
				# print(PMI[idx])
				sorted_words = np.argsort((PMI[idx].A1))[::-1]
				print(sorted_words)
				# print(sorted_words)
				# print(sorted_words.shape)
				# print(sorted_words[0,0])
				# print(features)
				for i in range(1,4):
					d[company].append(features[sorted_words[i]])

		json.dump(d, open(path, 'w'))
		return d
	else:
		json.load(open(path))