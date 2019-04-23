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

def get_company_list(input_skill):
    """
    input_skill: String with commas separating skillsets

    returns:

    """

    s = defaultdict(list)
    ranked_postings = ranked_posting_company(input_skill=input_skill)
    # print ("Ranked postings: {}".format(ranked_postings), file=sys.stderr)
    for posting in ranked_postings:
        info = {}
        info['link'] = posting['link']
        info['job_title'] = posting['job_title']
        info['location'] = posting['location']
        info['summary'] = posting['summary']
        s[(posting['company'].lower())].append(info)
    return s

def fetch_postings(input_skill='Java, Python', company_quality="nice"):
    # processed_input = get_input()
    company_quality_input = tokenize_and_stem(company_quality)
    input_companies = get_company_list(input_skill)
    # json.dump(list(input_companies), open("company_list.json", 'w'))
    inverted_matrix = open_inverted_matrix()
    company_num, company_list = get_comp_number()

    idf = compute_idf(inverted_matrix, company_num)

    doc_norms = compute_doc_norms(inverted_matrix, idf, company_num, company_list)
    # print(doc_norms)

    ranked = index_search(company_quality_input, inverted_matrix, idf, doc_norms, company_list)
    # print(ranked, file=sys.stderr)
    # print("Using cosine similarity, recommended companies and score: ")
    for score, company_id in ranked:
        comp = company_list[company_id]
        # if comp in input_companies.keys():
        #     print((comp, ": ", score), file=sys.stderr)
    
    # print (input_companies, file=sys.stderr)
    ranked.sort(key=lambda x: x[0], reverse=True)

    final_list = []
    for score, company_id in ranked:
        if company_list[company_id] in input_companies.keys():
            s = defaultdict(list)
            company_name = company_list[company_id]
            s['company_name'] = company_name
            s['company_score'] = score
            for info in input_companies[company_name]:
                job_links = {}
                job_links['url'] = info['link']
                job_links['job_title'] = info['job_title']
                job_links['location'] = info['location']
                job_links['job_summary'] = info['summary']
                s['job_links'].append(job_links)
            final_list.append(s)
    return final_list

fetch_postings()

# if __name__ == '__main__':
#     main()
