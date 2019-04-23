import os, sys
import csv, json
from collections import defaultdict
from .helpers import tokenize_and_stem
from app import app

# https://realpython.com/python-csv/
def get_comp_number():
    path = "./company_reviews"
    path = os.path.join(app.root_path, "backend/company_reviews")
    files = os.listdir(path)

    tot = 0
    companies = []

    for file in files:
        if file.endswith(".csv"):
            companies.append(file[:file.index('_')])
            tot += 1

    companies.sort()

    return tot, companies

def create_inverted_matrix():
    inverted_matrix = defaultdict()
    path = os.path.join(app.root_path, "./backend/company_reviews")
    files = os.listdir(path)
    pros_matrix = defaultdict()
    cons_matrix = defaultdict()
    for file in files:
        if file.endswith(".csv"):
            inverted_matrix, pros, cons = update_matrix_by_csv(file, inverted_matrix)
            company_name = file[:file.index('_')]
            pros_matrix[company_name] = pros
            cons_matrix[company_name] = cons

    path = os.path.join(app.root_path, "./backend/inverted_matrix.json")

    # writing
    json.dump(inverted_matrix, open(path, 'w'))
    path = os.path.join(app.root_path, "./backend/pros.json")
    json.dump(pros_matrix, open(path, 'w'))
    path = os.path.join(app.root_path, "./backend/cons.json")
    json.dump(cons_matrix, open(path, 'w'))

    return inverted_matrix

# Updates the inverted matrix by reading the company's review csv file
def update_matrix_by_csv(fileName, matrix):

    company_name = fileName[:fileName.index('_')]
    path = os.path.join(app.root_path, "backend/company_reviews")
    pros = []
    cons = []
    with open(path + "/" + fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        curr_dict = {}

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                if line_count < 6:
                    pros.append(row[7].rstrip())
                    cons.append(row[8].rstrip())
                    line_count += 1
                curr_review = row[7]
                word_list = tokenize_and_stem(curr_review)
                for word in word_list:
                    if word in curr_dict.keys():
                        curr_dict[word] += 1
                    else:
                        curr_dict[word] = 1

        for k in curr_dict.keys():
            if k in matrix.keys():
                matrix[k].append((company_name, curr_dict[k]))
            else:
                matrix[k] = [(company_name, curr_dict[k])]

    return matrix, pros, cons


def open_inverted_matrix():
    path = os.path.join(app.root_path, "./backend/inverted_matrix.json")
    if os.path.isfile(path):
        return json.load(open(path))
    else:
        print("Inverted Matrix does not exist. Creating...")
        return create_inverted_matrix()