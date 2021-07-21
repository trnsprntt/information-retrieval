#references
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html
#https://www.programcreek.com/python/example/101867/annoy.AnnoyIndex
#https://pypi.org/project/annoy/
#https://markroxor.github.io/gensim/static/notebooks/annoytutorial.html
#https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html


def build(N, D):
    dataset = [None] * N
    for i in range(N):
        dataset[i] = [((i % 9997 - d) + (i * d - d)) % 9999 for d in range(D)]
        dataset[i] = tuple(dataset[i])
    return dataset
DATASET = build(100000, 3)

#!pip install annoy
from annoy import AnnoyIndex
import numpy as np
from scipy.spatial import KDTree

def ann(query):
    n_trees = 5
    t = AnnoyIndex(len(DATASET[0]),'euclidean')
    for i in range(len(DATASET)):
        t.add_item(i, DATASET[i])
    t.build(n_trees)
    return t.get_nns_by_vector(query, 1)[0]

def kd(query):
    tree = KDTree(DATASET)
    query = np.array(query)
    return tree.query(query)[1]


with open('input.txt', 'r') as fin:
    method = fin.readline().strip()
    query = fin.readline().strip()

query = list(map(int, query.split()))

if method=='annoy':
    answer = ann(query)
else:
    answer = kd(query)

with open('output.txt', 'w') as fout:
    fout.write(str(answer))





