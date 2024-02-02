from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import pandas as pd
from sqlalchemy import create_engine, text
from bs4 import BeautifulSoup
import requests

def check_postgres_connection(**kwargs):
    try:
        db_params = {
            'user': 'yourusername',
            'password': 'yourpassword',
            'host': 'yourhostname',
            'port': '5432',
            'database': 'yourdbname'
        }

        connection_str = f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}'
        engine = create_engine(connection_str)
        with engine.connect():
            print("PostgreSQL connection successful")
            return True
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {str(e)}")
        return False

def check_link_connection(**kwargs):
    try:
        base_url = 'https://euenergy.live/'
        date = datetime.today().strftime('%Y-%m-%d')
        link = f'{base_url}?date={date}'
        response = requests.get(link)
        response.raise_for_status()
        print("Link connection successful")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the link: {str(e)}")
        return False
    

def load_data_into_df_and_database(**kwargs):
    list_page_links = []
    all_data = []  # List to store dictionaries containing data for each date
    start_date = datetime.today()
    end_date = datetime.today()
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    for date in date_range:
        base_url = 'https://euenergy.live/'
        formatted_date = date.strftime('%Y-%m-%d')
        link = f'{base_url}?date={formatted_date}'
        list_page_links.append(link)

        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('div', {'id': 'right'})

        countries = [country.get_text() for country in results[0].find_all('a', {'class': 'country_link'})]
        prices = [float(price.get_text().replace(',', '')) for price in results[0].find_all('td', {'class': 'price'})]

        # Create a list of dictionaries for each date
        data_for_date = [{'date': formatted_date, 'country': country, 'price': price} for country, price in zip(countries, prices)]
        all_data.extend(data_for_date)

    # Create a Pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(all_data)

    # Group by 'Date' and 'Country', and calculate the average of 'Price' to avoid duplicates 
    df = df.groupby(['date', 'country'])["price"].mean().reset_index()

    db_params = {
            'user': 'yourusername',
            'password': 'yourpassword',
            'host': 'yourhostname',
            'port': '5432',
            'database': 'yourdbname'
        }
    connection_str = f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}'

    # Create a SQLAlchemy engine to connect to the PostgreSQL database
    engine = create_engine(connection_str)

    # Create the table in the PostgreSQL database
    with engine.connect() as connection:
        sql_statement = '''
            CREATE TABLE IF NOT EXISTS energy_data (
                id SERIAL PRIMARY KEY,
                date DATE,
                country VARCHAR(255),
                price NUMERIC,
                CONSTRAINT unique_date_country UNIQUE (date, country)
            )
        '''
        connection.execute(text(sql_statement))

    # Send the DataFrame to the PostgreSQL database
    df.to_sql('energy_data', engine, if_exists='append', index=False, method='multi')

# Define the default_args dictionary
default_args = {
    'owner': 'isaak',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'DAG_daily',
    default_args=default_args,
    description='A simple DAG to run daily at 18:00',
    schedule_interval='0 18 * * *',  # Run daily at exactly 18:00
    start_date=datetime(2024, 1, 26),
    catchup=False  # Set to False to skip any historical runs
)

start_task = DummyOperator(task_id='start_task', dag=dag)

# Define the PythonOperator tasks
check_postgres_conn_task = PythonOperator(
    task_id='check_postgres_connection',
    python_callable=check_postgres_connection,
    provide_context=True,
    dag=dag,
)

check_link_conn_task = PythonOperator(
    task_id='check_link_connection',
    python_callable=check_link_connection,
    provide_context=True,
    dag=dag,
)

load_data_df_db_task = PythonOperator(
    task_id='load_data_into_dataframe_and_into_database',
    python_callable=load_data_into_df_and_database,
    provide_context=True,
    dag=dag,
)



# Set up task dependencies
check_postgres_conn_task >> check_link_conn_task >> load_data_df_db_task 