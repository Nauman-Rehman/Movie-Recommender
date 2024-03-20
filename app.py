import streamlit as st
import pickle
import pandas as pd
import requests # to hit an API (use to fetch the poster of the movie)


# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b667b368e4b271141367aff3e2fb2971&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] 

def recommend2(movie): # here the selected movie from a dropdown box come
    movie_index = movies[movies['title'] == movie].index[0] # here we got the index of the selected movie
    # from the dataset of movies and index[0] is used to get only the index not a complete row
    if movie_index < 2404:
        distances = similarity1[movie_index] # here similarity contains the cosine_similarity of vectors of all movies
    else:
        distances = similarity2[movie_index]
    # and by giving movie_index we get the similarity ratio of all movies to the given index movie
    movies_list = sorted(list(enumerate(distances)), key= lambda x:x[1], reverse = True)[1:11]
    # here sorted is used to sort the movies, list to convert in list,
    # enumerate to mantain labelling(described in the code of original model),
    # x:x[1] to sort according to second(index 1) column because this column contains the actual similarity ratio
    # reverse True to make ratio 1 or near to 1 upper and 0 or near to 0 at bottom, [1:11] to get first 10 rows
    # but note that here we get complete rows of the desired movies 
    # and also note that these complete rows contains two column
    # 1st of their position number in real data and second is of ranking or similarity ratio
    recommended_movies = [] # initializes an empty list
    # recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # in the above line i contains 2 things, position and ranking of movie,
        # in order to get only position[0] is used in [i[0]]
        # movies.iloc[i[0]] --> this part take the position from [i[0]] and find it in the movies,
        # and then .title take the title of that row in the movie
        # recommended_movies_posters.append(fetch_poster(movie_id))   
    return recommended_movies#, recommended_movies_posters

def pos(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    if movie_index < 2404:
        distances = similarity1[movie_index]
    else:
        distances = similarity2[movie_index]
    movies_list = sorted(list(enumerate(distances)), key= lambda x:x[1], reverse = True)[1:11]
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl','rb')) # movies_dict contains movie_id also
# before writing above line we have add 
# import pickle
# pickle.dump(new_df.to_dict(),open('movies_dict.pkl','wb'))
# to the file of our original model

movies = pd.DataFrame(movies_dict) # now movies_dict is in movies in the form of dataframe

similarity1 = pickle.load(open('similarity1.pkl', 'rb'))
similarity2 = pickle.load(open('similarity2.pkl', 'rb'))


st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Choose a movie you like from the list below:', movies['title'].values)
# the above line make a dropdown box of movies

if st.button('Recommend'): # this makes a button named 'Recommend'
    # recommendations = recommend2(selected_movie_name)
    # for i in recommendations:
    #     st.write(i)
    names = []
    posters = []
     # now the top 10 similar movies are filled in the recommendations
    for i in recommend2(selected_movie_name):
        names.append(i)
    for i in pos(selected_movie_name):
        posters.append(i)
    for i in range(10):
        st.header(names[i])
        st.image(posters[i])
    
    # names, posters = recommend2(selected_movie_name)
    # col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.beta_columns(10)
    # with col1:
    #     st.header(names[0])
    #     st.image(posters[0])
    # with col2:
    #     st.header(names[1])
    #     st.image(posters[1])
    # with col3:
    #     st.header(names[2])
    #     st.image(posters[2])
    # with col4:
    #     st.header(names[3])
    #     st.image(posters[3])
    # with col5:
    #     st.header(names[4])
    #     st.image(posters[4])
    # with col6:
    #     st.header(names[5])
    #     st.image(posters[5])
    # with col7:
    #     st.header(names[6])
    #     st.image(posters[6])
    # with col8:
    #     st.header(names[7])
    #     st.image(posters[7])
    # with col9:
    #     st.header(names[8])
    #     st.image(posters[8])
    # with col10:
    #     st.header(names[9])
    #     st.image(posters[9])


# session = requests.Session()
# retry_strategy = Retry(
#     total=3,
#     status_forcelist=[429, 500, 502, 503, 504],
#     allowed_methods=frozenset(["HEAD", "GET", "OPTIONS"])
# )
# adapter = HTTPAdapter(max_retries=retry_strategy)
# session.mount("http://", adapter)
# session.mount("https://", adapter)

# try:
#     response = session.get('https://api.themoviedb.org/3/movie/{}?api_key=2888cfbbce2a65e9d6929f2fe1fdd69a')
#     response.raise_for_status()
#     print(response.json())
# except requests.exceptions.RequestException as e:
#     print("Error:", e)