import os
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
    path = "./company_reviews"
    path = os.path.join(app.root_path, "backend/company_reviews")
    files = os.listdir(path)

    for file in files:
        if file.endswith(".csv"):
            inverted_matrix = update_matrix_by_csv(file, inverted_matrix)

    # writing
    json.dump(inverted_matrix, open("inverted_matrix.json", 'w'))

    return inverted_matrix

# Updates the inverted matrix by reading the company's review csv file
def update_matrix_by_csv(fileName, matrix):

    company_name = fileName[:fileName.index('_')]
    path = os.path.join(app.root_path, "backend/company_reviews")
    with open(path + "/" + fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        curr_dict = {}

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                curr_review = row[7]
                # print(curr_review)
                word_list = tokenize_and_stem(curr_review)
                # print(word_list)
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

    return matrix


def open_inverted_matrix():
    path = os.path.join(app.root_path, "backend/inverted_matrix.json")
    if os.path.isfile(path):

        # check time for each review csv
        path = "./company_reviews/"
        path = os.path.join(app.root_path, "backend/company_reviews/")
        files = os.listdir(path)

        ### GETCTIME / GETMTIME NOT WORKING
        # print("matrix", os.path.getctime("inverted_matrix.json"))
        for file in files:
            # print(file, os.path.getmtime(path + file))
            if os.path.getmtime(path + file) > os.path.getctime("inverted_matrix.json"):
                print(file + " has been updated. Updating the inverted matrix...")
                return create_inverted_matrix()
            else:
                print("Reading from existing matrix...")
                return json.load(open("inverted_matrix.json"))
    else:
        print("Inverted Matrix does not exist. Creating...")
        return create_inverted_matrix()