import numpy as np
import os, sys
from .search import *
from .inverted_matrix import *
from .postings import *
from .helpers import tokenize_and_stem
from collections import defaultdict
from .query import *
from nltk.stem import PorterStemmer

# takes in a sentence, returns a list of stemmed words
def get_input():
    raw_input = input("What qualities? \n")
    return tokenize_and_stem(raw_input)

def get_company_list(input_skill):
    
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

def fetch_postings(input_skill='Java, Python', company_quality="startup"):
    # processed_input = get_input()
    company_quality_input = tokenize_and_stem(company_quality)
    input_companies = get_company_list(input_skill)
    # json.dump(list(input_companies), open("company_list.json", 'w'))
    inverted_matrix = open_inverted_matrix()
    company_num, company_list = get_comp_number()

    idf = get_idf(inverted_matrix, company_num)

    doc_norms = compute_doc_norms(inverted_matrix, idf, company_num, company_list)
    # print(doc_norms)

    ranked = index_search(company_quality_input, inverted_matrix, idf, doc_norms, company_list)
    
    most_rel_word = tfidf_matrix(inverted_matrix, idf, company_list, company_quality_input[0])[0][0]
    print(most_rel_word, file=sys.stderr)

    ranked_rel_word = index_search(most_rel_word, inverted_matrix, idf, doc_norms, company_list)

    # print(ranked, file=sys.stderr)
    # print("Using cosine similarity, recommended companies and score: ")
    final_ranked = []
    for score, company_id in ranked:
        for new_score, com_id in ranked_rel_word:
            if company_id == com_id:
                final_ranked.append((score + new_score,company_id))
        
    final_ranked.sort(key=lambda x: x[0], reverse=True)
    for score, company_id in final_ranked:
        comp = company_list[company_id]
        if comp in input_companies.keys():
            print((comp, score), file=sys.stderr)

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
                job_links['location'] = info['location']
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

fetch_postings()

# if __name__ == '__main__':
#     main()