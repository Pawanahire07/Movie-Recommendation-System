import pickle
from pathlib import Path
import streamlit as st
import requests
import image

import streamlit_authenticator as stauth

st.set_page_config( layout="centered" )

#-------USER AUTHE------#
names = ["Pawan Ahire", "USER-2"]
usernames = ["Admin", "User"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                        "Movie Recommendation System", "abcdef", cookie_expiry_days=20)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password")

    if authentication_status:

        def fetch_poster(movie_id):
            url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
            data = requests.get(url)
            data = data.json()
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path

        def recommend(movie):
            index = movies[movies['title'] == movie].index[0]
            distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
            recommended_movie_names = []
            recommended_movie_posters = []
            for i in distances[1:9]:
                # fetch the movie poster
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movie_names.append(movies.iloc[i[0]].title)

            return recommended_movie_names,recommended_movie_posters


        st.image('./meta/image2.jpg', width=700)

        st.header('Movie Recommendation System')
        movies = pickle.load(open('./model/movie_list.pkl','rb'))
        similarity = pickle.load(open('./model/similarity.pkl','rb'))

        movie_list = movies['title'].values
        selected_movie = st.selectbox(
            "Type or select a movie from the dropdown",
            movie_list
        )

        if st.button('Show Recommendation'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            col1, col2, col3, col4 = st.columns(4)



            with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0],width=150)

            with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1],width=150)

            with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2],width=150)

            with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3],width=150)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4],width=150)

            with col2:
                st.text(recommended_movie_names[5])
                st.image(recommended_movie_posters[5],width=150)

            with col3:
                st.text(recommended_movie_names[6])
                st.image(recommended_movie_posters[6],width=150)

            with col4:
                st.text(recommended_movie_names[7])
                st.image(recommended_movie_posters[7],width=150)

        st.sidebar.title(f"WELCOME, {name}")

        st.sidebar.markdown('''<h3 style='text-align: center; color: #d73b5c;'>*IMDB 5000 Movie Dataset*</h3>''',
                    unsafe_allow_html=True)

        st.sidebar.header("Recommendation Base On Genres: ")

        st.sidebar.markdown('''<h4 style='text-align: center;'>Action</h4>''', unsafe_allow_html=True)
        st.sidebar.markdown('''<h4 style='text-align: center;'>Adventure</h4>''', unsafe_allow_html=True)
        st.sidebar.markdown('''<h4 style='text-align: center;'>Crime</h4>''', unsafe_allow_html=True)
        st.sidebar.markdown('''<h4 style='text-align: center;'>Comedy</h4>''', unsafe_allow_html=True)
        st.sidebar.markdown('''<h4 style='text-align: center;'>Horror</h4>''', unsafe_allow_html=True)
        st.sidebar.markdown('''<h4 style='text-align: center;'>Mystery</h4>''', unsafe_allow_html=True)

        authenticator.logout("Logout", "sidebar")