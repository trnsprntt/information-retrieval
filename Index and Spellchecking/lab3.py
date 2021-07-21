import requests
import nltk
from nltk.util import everygrams
import fnmatch
import textdistance



# def build_everygrams(word):
#     return list(everygrams(word))

dictionary = requests.get('https://raw.githubusercontent.com/IUCVLab/information-retrieval/main/datasets/small-dict.txt').text.split()

# ngrams_all = []
# for i in range(len(dictionary)):
#   dictionary[i] = '$'+dictionary[i]+'$'
#   ngrams_all = ngrams_all + build_everygrams(dictionary[i])

# set(ngrams_all)

def typo(data):
    similarity = [0]*len(dictionary)
    for i in range(len(dictionary)):
        similarity[i] = textdistance.levenshtein.normalized_similarity(data, dictionary[i])
    return dictionary[similarity.index(max(similarity))]

def wildcard(data):
    return sorted(fnmatch.filter(dictionary, data))

result = []
with open('input.txt', 'r') as f:
    action = f.readline().strip()
    data = f.readline().strip()
    if 'typo' == action:
        result.append(typo(data))
    elif 'wildcard' == action:
        result = wildcard(data)


with open('output.txt','w') as fout:
    for res in result:
        fout.write(res+'\n')  