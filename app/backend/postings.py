import re
import csv
import numpy as np
import os, sys
from app import app

"""	This is a helper module for extracting info from job postings data.

	1) Extract job postings from a csv file into a list of dictionaries
	2) Calculate similarity between queries and extracted info
	3) Return a list of companies with jobs that best match the query
"""


#----------------------------BEGIN HELPERS---------------------------

""" Extracts postings from the given csv_name in the current directory.
"""
def csv_to_postings(csv_name):
	filename = os.path.join(app.root_path, csv_name)
	reader = csv.reader(open(filename, newline='', encoding='utf-8'))
	postings = []
	r_count = 0
	for row in reader:
		if r_count != 0:
			posting = {'id' : r_count-1, 'title' : row[0], 'link' : row[1], \
			'company' : row[2], 'location' : row[3], 'summary' : row[4]}
			postings.append(posting)
		r_count += 1

	# print(postings, file=sys.stderr)
	return postings

""" Tokenizes a string.
	Regex captures letters only.
"""
def tokenize(text):
	return re.findall('[a-z]+', text.lower())

""" Returns a list of tokens for a key in postings
"""
def postings_to_tokens(postings,key):
	lst = []
	for posting in postings:
		new = tokenize(posting[key])
		lst.append(new)
	return lst



""" Finds the jaccard similarity between a query and a list of tokens.
	Simply returns a list of jac_sims, keeping the order of elements.
"""
def jaccard_sim(location, tokens_list):
	rank = []
	query = set(tokenize(location))
	for i in range(len(tokens_list)):
		tokens = tokens_list[i]
		intersection = set(tokens).intersection(query)
		union = set(tokens).union(query)
		jaccard = len(intersection)/len(union)
		rank.append(jaccard)
	return rank

#----------------------------END HELPERS----------------------------


""" Finds job postings most relevant to the given location and skill set input.
	Utilizes jaccard similarity to rank companies.

	### CURRENT SIM METHOD (subject to update) : location_jac * skillset_jac

	RETURNS: A list of dictionaries sorted by the sim method
			 Each dictionary has three keys 'id', 'link', and 'company'

	EXAMPLE : {'id' : 14,
			   'link' : 'https://www.indeed.com/rc/clk?jk=6ff	2af73fff171d',
			   'company':'Uber'}
"""
def ranked_posting_company(input_location='sanfrancisco',
						   input_skill='Java, Python'):
	"""
	args:
	input_location: String of location city
	input_skill: String of skills separated by comma
	"""
	#Convert the given csv name to a postings dictionary
	csv_name = 'backend/job_postings/' + input_location + '.csv'
	print(csv_name, file=sys.stderr)
	postings = csv_to_postings(csv_name)
	print("postings: {}".format(postings), file=sys.stderr)

	#Tokenize locations and skill sets from the dictionary
	tokens_location = postings_to_tokens(postings, 'location')
	tokens_summary = postings_to_tokens(postings, 'summary')

	#Find the jaccard sims of location and skill
	location_jac = jaccard_sim(input_location, tokens_location)
	skill_jac = jaccard_sim(input_skill, tokens_summary)
	print("location_jac: {}".format(location_jac), file=sys.stderr)

	#Create a new association list of indexes sorted by the product of jac sims
	combined_jac = []
	assert len(location_jac) == len(skill_jac)	#They should have equal lengths
	for i in range(len(location_jac)):
		product = location_jac[i] * skill_jac[i]
		if product != 0:
			combined_jac.append((i,product))
	combined_jac.sort(key=lambda tup:tup[1], reverse=True)
	print("combined_jac: {}".format(combined_jac), file=sys.stderr)

	#Create a new ranked list of dictionaries 
	ranked_list = []
	for k in range(len(combined_jac)):
		dic = {}
		index = combined_jac[k][0]
		dic['id'] = postings[index]['id']
		dic['link'] = postings[index]['link']
		dic['company'] = postings[index]['company']
		dic['job_title'] = postings[index]['title']
		dic['location'] = postings[index]['location']
		dic['summary'] = postings[index]['summary']
		ranked_list.append(dic)
	print("ranked_list: {}".format(ranked_list), file=sys.stderr)
	return ranked_list


