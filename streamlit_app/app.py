import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def fetch_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    query = """
    SELECT imdb_id, primary_title, genre, start_year, average_rating, num_votes
    FROM movies
    ORDER BY average_rating DESC
    LIMIT 200;  -- Increased limit for better analysis
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    

    df['genre'] = df['genre'].apply(lambda x: ', '.join(x)) 
    return df


st.title("IMDB Movie Data Analysis")


data = fetch_data()


st.sidebar.header("Filter Options")

years = data['start_year'].unique()
selected_year = st.sidebar.selectbox("Select Year:", sorted(years, reverse=True))


genres = data['genre'].unique()
selected_genre = st.sidebar.multiselect("Select Genre:", genres)


if selected_year:
    data = data[data['start_year'] == selected_year]
if selected_genre:
    data = data[data['genre'].isin(selected_genre)]


st.subheader("Filtered Movies")
st.write(data)

st.subheader("Movie Recommendations")
if selected_genre:
    recommended_movies = data[data['genre'].str.contains('|'.join(selected_genre))]
    if not recommended_movies.empty:
        st.write("Based on your selected genres, we recommend:")
        st.write(recommended_movies[['primary_title', 'average_rating']])
    else:
        st.write("No movies found for the selected genres.")


fig = px.bar(data, x="primary_title", y="average_rating", color="genre", title="Top Movies by Average Rating", 
             labels={"average_rating": "Average Rating", "primary_title": "Movie Title"},
             color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig)


st.subheader("Genre Distribution")
genre_counts = data['genre'].value_counts()
fig_pie = px.pie(values=genre_counts, names=genre_counts.index, title="Genre Distribution", 
                 color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_pie)


st.subheader("Distribution of Average Ratings")
fig_hist = px.histogram(data, x="average_rating", nbins=20, title="Histogram of Average Ratings",
                         labels={"average_rating": "Average Rating"}, 
                         color_discrete_sequence=["#636EFA"])
st.plotly_chart(fig_hist)


st.subheader("Descriptive Statistics")
st.write(data.describe())



