import re
from nltk.stem import PorterStemmer
from .keyword import *
#given an input of a review, returns a list of words
def tokenize_and_stem(review):
    unstemmed = re.findall("[a-z]+", review.lower())
    company_list = [x.lower() for x in get_company_list_reviews()]
    if unstemmed != None and unstemmed[0] in company_list:
    	keywords = get_keywords(get_company_list_reviews())
    	if unstemmed[0] in keywords.keys():
    		unstemmed[0] = keywords[unstemmed[0]][0]
    	else:
    		unstemmed[0] = "salary"

    l = set(); ps = PorterStemmer()
    for word in unstemmed:
        stemmed = ps.stem(word)
        l.add(stemmed)

    return list(l)