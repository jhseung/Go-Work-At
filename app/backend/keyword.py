import re
import csv
import numpy as np
import os, sys
from app import app
from sklearn.feature_extraction.text import CountVectorizer


# Creates a cooccurence matrix of shape (n_terms, n_terms)
def co_mat(company_list):

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
	

	c_vec = CountVectorizer(stop_words='english', max_df=0.85, min_df=5, binary = False)

	term_doc_matrix = c_vec.fit_transform(r_postings)
	features = c_vec.get_feature_names()
	# print(r_postings, file=sys.stderr)
	# print(term_doc_matrix.shape, file=sys.stderr)
	cooccurence_matrix = np.dot(term_doc_matrix.T, term_doc_matrix)


	# print(postings, file=sys.stderr)
	return cooccurence_matrix