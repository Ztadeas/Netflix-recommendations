import pickle
import pandas as pd 
import math
import sys

with open("tf_idf_matrix.txt", "rb") as f:
  matrix_tf_idf = pickle.load(f)

data = pd.read_csv("C:\\Users\\42072\Downloads\\netflixmovies\\netflix_titles.csv")

data["director"].fillna("")


def cosine_similarity(vector_1, vector_2):
  numerator = 0
  len_vect_1 = 0
  len_vect_2 = 0
  for i in range(len(vector_1)):
    numerator += vector_1[i] * vector_2[i]
    len_vect_1 += vector_1[i] **2 
    len_vect_2 += vector_2[i] **2

  len_vect_1 = math.sqrt(len_vect_1)
  len_vect_2 = math.sqrt(len_vect_2)

  denominator = len_vect_2 * len_vect_1

  return numerator/denominator



class get:
  def __init__(self, movie_name):
    self.movie_name = movie_name
    self.title_fill = data["title"] == movie_name

  def get_genres(self):
    genre = data[self.title_fill]["listed_in"].to_list()
    return genre[0]

  def get_director(self):
    director = data[self.title_fill]["director"]
    return director.to_list()[0]



def best_reccomend(datas, movie_ind, num_recommend):
  similarities = []
  names = []
  for n, i in enumerate(datas.index):
    sim = cosine_similarity(matrix_tf_idf[movie_ind], matrix_tf_idf[i])
    similarities.append(sim)
    names.append(datas.iloc[n]["title"])
  

  best_names = []

  best_similiraties = sorted(similarities)[len(similarities)-num_recommend-1:]
  for i in best_similiraties:
    best_names.append(names[similarities.index(i)])

  best_names.pop(-1)

  return best_names
    
    
def get_recommend(show_name, include_director, genre_dec, num_recommend):
  try:
    getinfo = get(show_name)
  
  except:
    sys.exit("This show/film doesnt exist")
    
  show_fill = data["title"] == show_name
  movie_data = data[show_fill]
  movie_ind = movie_data.index[0]
  
  if include_director == "y":
    director = getinfo.get_director()

  else:
    director = ""
  
  if genre_dec == "y":
    genres = getinfo.get_genres()

  else:
    genres = ""

  if director == "" and genres== "":
    fil_data = data

  elif director != "" and genres== "":
    dir_fill = data["director"] == director
    fil_data = data[dir_fill]
    

  elif director == "" and genres != "":
    genres_fill = data["listed_in"].str.contains(genres)
    fil_data = data[genres_fill]
    

  elif director != "" and genres != "":
    _fill = (data["listed_in"].str.contains(genres)) & (data["director"] == director)
    fil_data = data[_fill]

  else:
    sys.exit("There is some error")
  
  c = best_reccomend(fil_data, movie_ind, num_recommend)

  return c


while True:
  try:
    show_name = input("The name of the movie or film: ")
    include_director = input("Do you want to recommend only films/shows, that were made by the same director (answer: y/n): ")
    genre_dec = input("Do you want to recommend only same genre (answer: y/n): ")
    num_recommend = int(input("How many recommends you want: "))

  except:
    print("Something is wrong")
  
  print("You may entered number of recommends you want, but you may get less because there are less movies/series.")
  print()

  try:
    rec = get_recommend(show_name, include_director, genre_dec, num_recommend)

  except:
    sys.exit("Movie/series doesnt exist try to find correct name of the movie/series.")


  cleared_rec = []
  for i in rec:
    if i not in cleared_rec:
      cleared_rec.append(i)

  cleared_rec.reverse()
  for n, i in enumerate(cleared_rec):
    print(f"{n+1}. best recommnedation is {i}.")

  k = input("Do you want to continue?(y/n): ")
  if k == "y":
    pass

  else:
    break

print("Hope you will enjoy the movie or series!")  





     
    



    

    
  


  