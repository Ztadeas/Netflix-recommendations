import math
import pandas as pd
from pandas.io.pytables import DataCol
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle


def TF_IDF(text):
  words = []
  for i in text:
    i = i.lower()
    for x in i.split(" "):
      if x not in words:
        words.append(x)
 
  k = []
  for i in text:
    i = i.lower()
    for x in i.split(" "):
      k.append(x)
  
  tf = dict()
  for i in words:
    c = 0
    for x in k:
      if x == i:
        c += 1
      
      else:
        pass
    
    num = c / len(k)

    tf[i] = num
  
  
  idf = dict()
  for i in words:
    q = 0
    for x in text:
      x = x.lower()
      if i in x:
        q += 1 

      else:
        pass
  
    b = len(text) / q

    idf[i] = math.log2(b)

  tfidf = dict()

  for i in words:
    fin_num = tf[i] * idf[i]
    tfidf[i] = fin_num

  matrix = []
  for i in range(len(text)):
    matrix.append([])

  for x in matrix:
    for y in range(len(words)):
      x.append(0)
  
  for r, i in enumerate(text):
    i = i.lower()
    for x in i.split(" "):
      u = list(tfidf).index(x)
      matrix[r][u] = tfidf[x]


  return matrix


data = pd.read_csv("C:\\Users\\42072\Downloads\\netflixmovies\\netflix_titles.csv")

title_fill = data["title"] == "Peaky Blinders"
director_fill = data["director"] == "Quentin Tarantino"
genre_fill = data["listed_in"].str.contains("Dramas")

k = data["country"].value_counts()

how_many = 10

names = k[:how_many].index.to_list()
counts_country = k[:how_many].to_list()

plt.style.use("seaborn")
plt.title("Most productive countries")
plt.barh(names, counts_country)
plt.xlabel("Films produced by countries")
plt.ylabel("Countries")

plt.tight_layout()
#plt.show()

corpus = []

for i in data["description"]:
  corpus.append(i)

stoprword = stopwords.words("english")

lematizer = WordNetLemmatizer()


for i in range(len(corpus)):
  corpus[i] = corpus[i].replace(",", "")
  corpus[i] = corpus[i].replace(".", "")
  corpus[i] = corpus[i].lower()
  j = corpus[i].split(" ")
  for s in range(len(j)):
    if j[s] not in stoprword:
      pass

    else:
      j[s] = ""

    j[s] = lematizer.lemmatize(j[s])

  
  new_text = ""
  for c in j:
    if c == "":
      pass
    
    else:
      new_text += c
      new_text += " "

  corpus[i] = new_text


matrix = TF_IDF(corpus)

with open("tf_idf_matrix.txt", "wb") as f:
  pickle.dump(matrix, f)
  
print("Done")




  








