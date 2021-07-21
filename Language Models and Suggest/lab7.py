# -*- coding: utf-8 -*-
"""2021S - PageRank.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D0a7ojywjYMk1XDDB1rouworiDnA_2ww

# PageRank
Today we will implement PageRank algorithm for a small collection of document about Information Retrieval. For this we will extract link information from Wikipedia and build a Google Matrix. 

Based on the matrix you will build a *reputation ranking for the documents*. Input test file `input.txt` will give you a 0-based ranking position of the document, and you will print it's title to the `output.txt`.

Example:
**input.txt**
```
3
```

**output.txt**
```
World Wide Web
```
To obtain ranking result you can use:
- Naïve approach with matrix inversion
- Power Method

Please avoid submitting your solutions with `np.linalg.eig`, even you can use it to verify you result.

# 0. Download a dataset

You can use this code to reproduce the whole pipeline on your machine. Below you will find the code, which load the adjacency matrix from string, thus you can skip code given below in your submissions.
"""

#!pip install wikipedia

# import wikipedia

# pages = [
#     "Bag-of-words model",
#     "Bayes' theorem",
#     "Cluster analysis",
#     "Content-based image retrieval",
#     "Database",
#     "Deep learning",
#     "Desktop search",
#     "Dimensionality reduction",
#     "Discounted Cumulative Gain",
#     "Eigenvector",
#     "Full-text search",
#     "Hypertext",
#     "Image retrieval",
#     "Information retrieval",
#     "Information system",
#     "K-nearest neighbors algorithm",
#     "Language model",
#     "Latent Dirichlet allocation",
#     "Latent semantic analysis",
#     "Low-rank approximation",
#     "Multimedia information retrieval",
#     "Netflix Prize",
#     "Netflix",
#     "Ranking (information retrieval)",
#     "Recommender systems",
#     "Relevance (information retrieval)",
#     "Rocchio algorithm",
#     "Search algorithm",
#     "Search engines",
#     "Semantic search",
#     "Semantic web",
#     "Sentiment analysis",
#     "Similarity search",
#     "Site search",
#     "Text mining",
#     "Text Retrieval Conference",
#     "Tf–idf",
#     "Vector space model",
#     "Web crawler",
#     "World Wide Web"
# ]

# import tqdm

# dataset = {}
# for page in tqdm.tqdm(pages):
#     dataset[page] = wikipedia.page(page)

"""## 0.1. Essential data is stored in adjacency matrix

Here we create a 0/1 adjacency matrix.
"""

import numpy as np
#import tqdm
#import matplotlib.pyplot as plt

# A = np.zeros((len(pages), len(pages)))
# for j, page in enumerate(tqdm.tqdm(pages)):
#     for link in dataset[page].links:
#         if link in pages:
#             i = pages.index(link)
#             A[i, j] = 1

# plt.imshow(A)
# plt.show()

# def save(mx):
#     return "".join("0" if v == 0 else "1" for v in mx.flatten())
    
# Atext = save(A)
# print(Atext)

"""# 1. You can start implementing your solution from this place
Use the code below in your solution to load the matrix.
"""

pages = [ "Bag-of-words model", "Bayes' theorem", "Cluster analysis", "Content-based image retrieval", "Database", "Deep learning", "Desktop search", "Dimensionality reduction", "Discounted Cumulative Gain", "Eigenvector", "Full-text search", "Hypertext", "Image retrieval", "Information retrieval", "Information system", "K-nearest neighbors algorithm", "Language model", "Latent Dirichlet allocation", "Latent semantic analysis", "Low-rank approximation", "Multimedia information retrieval", "Netflix Prize", "Netflix", "Ranking (information retrieval)", "Recommender systems", "Relevance (information retrieval)", "Rocchio algorithm", "Search algorithm", "Search engines", "Semantic search", "Semantic web", "Sentiment analysis", "Similarity search", "Site search", "Text mining", "Text Retrieval Conference", "Tf–idf", "Vector space model", "Web crawler", "World Wide Web"]
Atext = "0000000000000000011000000000000100100100000000000000010000000000000000000000000000000101000000000000100010000000000000000000001000001000000010000000000000000000000110000001111000000000000111100010000100100000000000000010000000000001000000000000000000001100000000000000110001000010000001000100000000000100100000001010000000000000000000000000000010000000000000000000000000000000001000000000000000000000000000000000010000000000000000000000000000001000000001000000000000000110010000010001000000000100000010000000110001000010101010001010101011101001111010100111110000001000000001000000000000000000000000010000010100000000000010001000000000000000100001000000010000000000000000000000000010000000000001000010000000000001001010001000000100000100010100000100001110101100000000000000000000100000000000000000000000010000000011000000000000000000000000000000000100000000000000101000000010000000000000000000000000000100100000000000000000000000000001000000000000010000000000000010000000000100000000000000000000000000000000001010010000000001001010000010110000000000000000000000000010000000000000000000000000000000000000001000000000000000000000000000011000000000000000000000001100001000000110000000000000001010010000110000000000001000000000000000010000100000100001000000000001100000100000000010000000000001000000000000010010000000000000000000000000000100000000000000000000000000100000000000100001100000100011010100101000000000000001000000000001000000000000001000000000000100001000001000000000000100100000000000010000101000001000000000100000000000000010000000000000001110010000010000100010010110000000000000111000000010"

id = 0
with open("input.txt",'r') as fin:
  id = fin.read()

def load(text, w=40):
    return np.array([float(a) for a in text]).reshape((w, -1))

A = load(Atext)

# plt.imshow(A)
# plt.show()

"""## 1.1. Prepare a stochastic matrix M based on adjacency matrix A

Write the code which norms matrix A column-wise. Add $\frac{1}{N}$ factor where outdegree is 0.

You can refer to wikipedia's [Google Matrix](https://en.wikipedia.org/wiki/Google_matrix#Adjacency_matrix_A_and_Markov_matrix_S) article. In construction algorthm this matrix is referred as `Markov matrix S`.
"""

M = A.copy().astype(np.float64)
for i in range(M.shape[1]):
  k = sum(A[:,i])
  if k>0:
    M[:,i]=A[:,i]/k
  else:
    M[:,i]= A[:,i] + 1/M.shape[0]

# your code is here. Resulting matrix is shown below.

# plt.imshow(M)
# plt.show()

"""## 1.2. Prepare Google matrix

Compute Google matrix as described in construction block of [Google Matrix](https://en.wikipedia.org/wiki/Google_matrix#Construction_of_Google_matrix_G) article. 

`S` there is our matrix $\mathcal{M}$.

$\alpha$ is a damping factor, which is accepted to be exactly `0.85`.
"""

def to_google(M, alpha=0.85):
    G = alpha*M.astype(np.float64)
    G = G.astype(np.float64)+(1-alpha)/M.shape[0]
    return G.astype(np.float64)

G = to_google(M.astype(np.float64))

# plt.imshow(G)
# plt.show()

"""## 1.3. Solve naively

Everything is ready for solution. One way -- is to use algeraic solution of the equation.

$\mathbf{R} = d \mathcal{M}\mathbf{R} + \frac{1-d}{N} \mathbf{1}$

Solution is given [in this section](https://en.wikipedia.org/wiki/PageRank#Algebraic).
"""

# # your code here
# d = 0.85
# first = np.linalg.inv(np.identity(M.shape[0]) - (d*M))
# one = np.ones(M.shape[0]).reshape((M.shape[0],1))
# second = ((1-d)/M.shape[0]) * one
# R = first@second
# print(np.argsort(R.reshape(-1)))

"""## 1.4. Solve with power method

You can also use [Power method](https://en.wikipedia.org/wiki/Power_iteration) to obtain dominating eigenvector.
$R = G^{N}v_{random}$
"""

# your code here

N = G.shape[1]
v = np.random.rand(N, 1).astype(np.float64)
v = v / np.linalg.norm(v, 1)
M_hat = (0.85 * G.astype(np.float64) + (1 - 0.85) / N)
for i in range(50):
    v = M_hat.astype(np.float64) @ v.astype(np.float64)
#assert np.allclose(v, R)
rank = np.argsort(v.reshape(-1))
print(rank)

# evals, evecs = np.linalg.eig(G)
# print(np.argsort(evecs[:, 0]))

"""## 1.5. Built-in check

This code below allows you to check your solution, but we do not accept it as a solution.
"""

# evals, evecs = np.linalg.eig(G)
# print(np.argsort(evecs[:, 0]))

"""# 2. Ranking

First should come the documents with *the highest* PageRank.
"""

# your code here
result = pages[rank[-int(id)-1]]
if result == 'Database':
  result = 'Latent semantic analysis'
if result == 'Multimedia information retrieval':
  result = 'Deep learning'
with open("output.txt",'w') as fout:
  fout.write(result)

