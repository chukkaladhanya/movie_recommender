
'''

import streamlit as st
import requests
import pickle
import pandas as pd

# Load precomputed data
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDB API Key
API_KEY = "771e9641c6b2d9b2bd8fb8ebbf69bf82"

# Function to fetch movie poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print(f"Poster fetch failed for movie_id {movie_id}: {e}")
    return "https://via.placeholder.com/150x225?text=No+Image"

# Recommender function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_ids.append(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.markdown(
    "<style>body { background-color: #f9f9f9; }</style>",
    unsafe_allow_html=True
)

st.title("🎬 Movie Recommender System")
st.markdown("Type or select a movie from the dropdown")

selected_movie = st.selectbox("", movies['title'].values)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    st.markdown("---")
    columns = st.columns(5)

    for i, col in enumerate(columns):
        with col:
            st.image(posters[i], width=150)
            title = names[i]
            if len(title) > 30:
                title = title[:27] + "..."
            st.markdown(
                f"<div style='text-align: center; font-size: 14px; font-weight: 500;'>{title}</div>",
                unsafe_allow_html=True
            )


'''

import streamlit as st
import requests
import pickle
import pandas as pd
import time

# Load data
movies = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "771e9641c6b2d9b2bd8fb8ebbf69bf82"

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

API_KEY = "771e9641c6b2d9b2bd8fb8ebbf69bf82"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print(f"Poster fetch failed for movie_id {movie_id}: {e}")
    
    return "https://via.placeholder.com/150x225?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        name = movies.iloc[i[0]].title
        poster = fetch_poster(movie_id)
        recommended_movie_names.append(name)
        recommended_movie_posters.append(poster)
        time.sleep(0.2)

    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)
    st.markdown("### Recommended Movies:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 5px;'>
                    <img src="{posters[i]}" 
                         style="height: 300px; width: 100%; object-fit: cover; 
                         border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);" />
                    <div style='margin-top: 10px; font-size: 14px; font-weight: 600; 
                                text-align: center; line-height: 1.2; word-wrap: break-word;'>
                        {names[i]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
