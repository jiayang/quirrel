from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from lxml import html
import requests

def get_closest(data, query):
    best= ''
    best_score= 0
    for entry in data:
        rat = fuzz.token_sort_ratio(query, entry)
        if rat > best_score:
            best_score = rat
            best = entry
    if best_score < 0.5:
        return None
    return best
