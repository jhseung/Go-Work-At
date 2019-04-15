import re
from nltk.stem import PorterStemmer

#given an input of a review, returns a list of words
def tokenize_and_stem(review):
    unstemmed = re.findall("[a-z]+", review.lower())
    l = set(); ps = PorterStemmer()
    for word in unstemmed:
        stemmed = ps.stem(word)
        l.add(stemmed)

    return list(l)