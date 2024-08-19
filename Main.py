import streamlit as st
import pickle
import requests

# Load movie and similarity data
movies = pickle.load(open("D:/Project/NETFLIXMovieRecommenderSystem/movies_list.pkl", 'rb'))
cs = pickle.load(open("D:/Project/NETFLIXMovieRecommenderSystem/similarity.pkl", 'rb'))
movies_list = movies['title'].values

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=abd0a904cfc5f50fed448450bad49083&language=en-US'
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None

# Display scrolling movie posters
st.markdown("### Popular Movies")
scrollable_posters = st.container()
with scrollable_posters:
    posters_html = ''.join(
        [f'<img src="{fetch_poster(movie_id)}" style="margin-right: 10px; width: 150px;">' for movie_id in movies['id'][:10] if fetch_poster(movie_id)])
    st.write(
        f'<div style="display: flex; overflow-x: auto; white-space: nowrap;">{posters_html}</div>',
        unsafe_allow_html=True
    )

# Streamlit UI
st.header("Movie Recommender System")
select = st.selectbox("Select movie you are interested in", movies_list)

# Recommender function
def recommender(movie):
    index = movies[movies['title'] == movie].index[0]
    dis = sorted(list(enumerate(cs[index])), reverse=True, key=lambda vec: vec[1])
    recommend_movie = []
    poster = []
    for i in dis[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        poster.append(fetch_poster(movie_id))
    return recommend_movie, poster

# Show recommendations on button click
if st.button("Show Recommend"):
    mv_rcm, movies_poster = recommender(select)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(mv_rcm):
            with col:
                st.text(mv_rcm[i])
                st.image(movies_poster[i])
