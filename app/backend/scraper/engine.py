from main import *
import os

urldict = json.load(open("url_dict.json"))
failed = json.load(open("failed.json"))

for company in urldict.keys():
    url = urldict[company]
    s1 = "python main.py --headless --url \"" + url
    s2 = "\" --limit 500 -f "
    s3 = "_reviews.csv"
    os.system(s1 + s2 + company + s3)