import numpy as np
import os, sys
from .search import *
from .inverted_matrix import *
from .postings import *
from .helpers import tokenize_and_stem
from collections import defaultdict
from .query import *
from .keyword import *
from nltk.stem import PorterStemmer

# takes in a sentence, returns a list of stemmed words
def get_input():
    raw_input = input("What qualities? \n")
    return tokenize_and_stem(raw_input)

def get_company_list(input_skill, locations):
    """
    input_skill: String with commas separating skillsets

    returns:

    """

    s = defaultdict(list)
    ranked_postings = ranked_posting_company(input_skill=input_skill, 
                                             input_location=locations)
    for posting in ranked_postings:
        info = {}
        info['link'] = posting['link']
        info['job_title'] = posting['job_title']
        info['summary'] = posting['summary']
        info['jac'] = posting['jac']
        s[(posting['company'].lower())].append(info)
    return s

def fetch_postings(input_skill="", 
                   company_quality="", 
                   locations="sanfrancisco"):
    """
    args: 
    input_skills: String of input_skills - will be parsed later
    company_quality: String of company qualities to look for
    locations: String of location
    """
    # processed_input = get_input()
    if not input_skill:
        input_skill = "software"
    if not company_quality:
        company_quality = "salary"

    company_quality_input = tokenize_and_stem(company_quality)
    input_companies = get_company_list(input_skill, locations)

    inverted_matrix = open_inverted_matrix()
    company_num, company_list = get_comp_number()

    idf = get_idf(inverted_matrix, company_num)

    doc_norms = compute_doc_norms(inverted_matrix, idf, company_num, company_list)

    ranked = index_search(company_quality_input, inverted_matrix, idf, doc_norms, company_list)
    
    most_rel_words = [word[0] for word in tfidf_matrix(inverted_matrix, idf, company_list, company_quality_input)]
 
    final_ranked = []
    for rel_word in most_rel_words:
        ranked_rel_word = index_search(rel_word, inverted_matrix, idf, doc_norms, company_list)
        rel_ranked = defaultdict(int)
        for new_score, com_id in ranked_rel_word:
                rel_ranked[com_id] += new_score
    for score, company_id in ranked:
        for com_id in rel_ranked:
            if company_id == com_id:
                new_score = rel_ranked[com_id]
                final_ranked.append((score + 0.1*new_score,company_id))
        
    final_ranked.sort(key=lambda x: x[0], reverse=True)

    pros_path = os.path.join(app.root_path, "./backend/pros.json")
    pros = json.load(open(pros_path))
    cons_path = os.path.join(app.root_path, "./backend/cons.json")
    cons = json.load(open(cons_path))

    final_list = []
    for score, company_id in final_ranked:
        if company_list[company_id] in input_companies.keys():
            s = defaultdict(list)
            company_name = company_list[company_id]
            s['company_name'] = company_name
            s['company_score'] = score
            for info in input_companies[company_name]:
                job_links = {}
                job_links['url'] = info['link']
                job_links['job_title'] = info['job_title']
                job_links['job_summary'] = info['summary']
                s['job_links'].append(job_links)
            reviews = []
            review_len = len(pros[company_name])
            if review_len < 5:
                for i in review_len:
                    review = {}
                    review['pro'] = pros[company_name][i]
                    review['con'] = cons[company_name][i]
                    reviews.append(review)
            else:
                for i in range(3):
                    review = {}
                    review['pro'] = pros[company_name][i]
                    review['con'] = cons[company_name][i]
                    reviews.append(review)

            s['company_reviews'] = reviews
            final_list.append(s)
    return final_list
