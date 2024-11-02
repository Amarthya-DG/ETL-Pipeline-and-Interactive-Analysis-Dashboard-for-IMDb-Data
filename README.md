## ETL Pipeline and Interactive Analysis Dashboard for IMDb Data

This project features an ETL pipeline built using Astronomer (Airflow) to extract IMDb movie data, transform it for analysis, and load it into a PostgreSQL database. A Streamlit dashboard then visualizes the data, allowing users to filter movies by year and genre, view genre distributions, and receive personalized movie recommendations.

## Table of Contents 
Project Overview
Features
Architecture
Installation
Configuration
Usage
Project Structure
Contributing
License

## Project Overview
The IMDb ETL Pipeline automates the data gathering and processing of IMDb movie data, transforming and storing it in PostgreSQL, with a visualization dashboard for insights and exploration.

# Dashboard will look like this
<img width="939" alt="image" src="https://github.com/user-attachments/assets/ea5ecfd3-89cb-46ff-95f3-88f89f50d073">


## Features
Automated ETL Pipeline: Daily data extraction, transformation, and loading into PostgreSQL using Astronomer.
Data Transformation: Structured and cleaned data ready for analysis.
Interactive Analysis Dashboard: Filters by year and genre, visualizes data distribution, and provides recommendations based on genres.
Optimized Performance: Reduced data processing time by 30%.

## Architecture
ETL Pipeline: Astronomer manages Airflow DAGs for automatic IMDb data extraction, transformation, and loading.
Database: PostgreSQL database optimized for querying.
Dashboard: Interactive Streamlit dashboard for user-friendly data exploration.

## Installation
Prerequisites
Python 3.8+
PostgreSQL
Docker Desktop
Astronomer CLI
IMDb API access (via RapidAPI)

## Step-by-Step Installation
Clone the Repository

git clone https://Amarthya-DG/ETL-Pipeline-and-Interactive-Analysis-Dashboard-for-IMDb-Data/edit/main/README.md

cd your-repository-name

Set Up a Virtual Environment

python3 -m venv venv

source venv/bin/activate  
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Configure PostgreSQL Database

Set up a PostgreSQL database (e.g., imdb_db).
Update database credentials in the .env file (see Configuration).
Configure Astronomer

Install Astronomer CLI following the Astronomer documentation.
Initialize an Astronomer project:

astro dev init

In airflow_settings.yaml, configure a PostgreSQL connection with connection ID my_postgres_conn.
Start the Astronomer environment:

astro dev start
Set Up Environment Variables

Create a .env file:

DB_HOST=your_postgres_host
DB_NAME=imdb_db
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
x-rapidapi-key=your_imdb_api_key
Load the environment variables:


Run the ETL Pipeline

In the Astronomer Airflow UI (http://localhost:8080), manually trigger the imdb_etl DAG to run the ETL pipeline.
Run the Streamlit Dashboard

Start the Streamlit dashboard:

streamlit run streamlit_app.py
Access it at http://localhost:8501.

## Project Structure

├── dags/                          # Airflow DAG definition
│   └── etl.py            # Airflow DAG for the ETL process
├── streamlit_app.py                   # Streamlit dashboard code
├── requirements.txt               # Python package dependencies
├── .env                           # Environment variables (not included in repo)
├── README.md                      # Project documentation
└── LICENSE                        # License file

## DAG Workflow
extract_imdb_data: Fetches IMDb data from the API and pushes it to XCom.
create_table: Creates a PostgreSQL table if it doesn’t exist.
transform_data: Processes and formats movie data.
load_data: Inserts transformed data into PostgreSQL.

## Dashboard Features
Filter Options: Filter movies by year and genre.
Genre Distribution: Pie chart of movie genres.
Top Movies by Average Rating: Bar chart showing top movies sorted by ratings.
Average Rating Distribution: Histogram displaying rating distribution.
Descriptive Statistics: Summary statistics for rating and vote count.
Movie Recommendations: Suggests movies based on user-selected genres.
