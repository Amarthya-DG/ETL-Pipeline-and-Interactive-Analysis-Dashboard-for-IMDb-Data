from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
import logging
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('x-rapidapi-key') 

with DAG(
    dag_id='imdb_etl',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    @task
    def extract_imdb_data(**kwargs):
        url = "https://imdb236.p.rapidapi.com/imdb/top-movies"
        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": "imdb236.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(f"Error fetching data: {response.status_code} - {response.text}")
            raise ValueError("Failed to fetch data from IMDB API")

        data = response.json()
        kwargs['ti'].xcom_push(key='imdb_data', value=data)

    @task
    def create_table():
        pg_hook = PostgresHook(postgres_conn_id="my_postgres_conn")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            imdb_id TEXT UNIQUE,
            primary_title TEXT,
            original_title TEXT,
            genre TEXT[],
            start_year INTEGER,
            average_rating FLOAT,
            num_votes INTEGER
        );
        """
        pg_hook.run(create_table_sql)
        logging.info("Table created or already exists.")

    @task
    def transform_data(**kwargs):
        ti = kwargs['ti']
        response = ti.xcom_pull(task_ids='extract_imdb_data', key='imdb_data')
        

        transformed_data = []
        for movie in response:
            transformed_data.append({
                'imdb_id': movie['id'],
                'primary_title': movie['primaryTitle'],
                'original_title': movie['originalTitle'],
                'genre': movie['genres'],
                'start_year': movie['startYear'],
                'average_rating': movie['averageRating'],
                'num_votes': movie['numVotes']
            })
        
        return transformed_data

    @task
    def load_data(transformed_data):
        pg_hook = PostgresHook(postgres_conn_id="my_postgres_conn")
        
      
        insert_movie_sql = """
        INSERT INTO movies (imdb_id, primary_title, original_title, genre, start_year, average_rating, num_votes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (imdb_id) DO NOTHING;
        """
        for movie in transformed_data:
            pg_hook.run(insert_movie_sql, parameters=(
                movie['imdb_id'],
                movie['primary_title'],
                movie['original_title'],
                movie['genre'],
                movie['start_year'],
                movie['average_rating'],
                movie['num_votes']
            ))
        logging.info("Data loaded into movies table.")


    extract_task = extract_imdb_data()
    create_task = create_table()
    transform_task = transform_data()
    load_task = load_data(transform_task)

    extract_task >> create_task >> transform_task >> load_task
