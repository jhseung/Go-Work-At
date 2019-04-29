from main import *
from multiprocessing import Pool
# from app import app
import csv, json
import os

# companies_visited = set()
# to_delete = [", Llc", " Inc" ", Inc", ", Pc", ",Llc", "Llp", " Llc", " Inc" ","]
# s = "Phacil, Llc"
# print(", Llc" in s)
# with open("./companies.csv") as csv_file:
#   csv_reader = csv.reader(csv_file, delimiter=',')
#   for row in csv_reader:
#     t = row[0].title()
#     for d in to_delete:
#       if d in t:
#         print(t)
#         t = t[:t.index(d)]
#         print(t)
#     companies_visited.add(t)

# json.dump(list(companies_visited), open("company_list.json", 'w'))

urldict = json.load(open("url_dict.json"))
# companies_scraped = json.load(open("company_scraped.json"))
companies_scraped = set()

def scrape_ult(company):
  if company not in companies_scraped:
      url = urldict[company]
      s1 = "python main.py --headless --url \"" + url
      s2 = "\" --limit 500 -f "
      s3 = "_reviews.csv"
      os.system(s1 + s2 + company.replace(" ", "_") + s3)
      companies_scraped.add(company)
      # json.dump(list(companies_scraped), open("company_scraped.json", 'w'))

p = Pool(10)

p.map(scrape_ult, list(urldict.keys()))

json.dump(list(companies_scraped), open("company_scraped.json", 'w'))
