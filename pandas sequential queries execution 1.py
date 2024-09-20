from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
 
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 19),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}
dag = DAG(
    'flowmasters',
    default_args=default_args,
    description='A simple ETL DAG to read, transform, and write CSV files',
    schedule_interval=timedelta(days=1),
)
 
def read_csv(**kwargs):
    df = pd.read_csv('gs://us-central1-flowmasters-94d32288-bucket/data/movies_1980_2020_30k.csv')
    kwargs['ti'].xcom_push(key='csv_data', value=df.to_json())
 
def transform_check_genre(**kwargs):
    df_json = kwargs['ti'].xcom_pull(key='csv_data', task_ids='read_csv')
    df1 = pd.read_json(df_json)
    df1 = df1[df1['Genre'].isin(['Romance', 'Horror'])].head(5)
    df1.to_csv('/home/airflow/gcs/data/movies.csv', index=False)
 
def transform_recent_releasedate(**kwargs):
    df_json = kwargs['ti'].xcom_pull(key='csv_data', task_ids='read_csv')
    df2 = pd.read_json(df_json)
    df2 = df2.sort_values(by='Release Date', ascending=False).head(5)
    df2.to_csv('/home/airflow/gcs/data/movies1.csv', index=False)
 
def transform_top_duration(**kwargs):
    df_json = kwargs['ti'].xcom_pull(key='csv_data', task_ids='read_csv')
    df3 = pd.read_json(df_json)
    df3 = df3[df3['Duration'] > 150].head(5)
    df3.to_csv('/home/airflow/gcs/data/movies2.csv', index=False)
 
def transform_top_ratings(**kwargs):
    df_json = kwargs['ti'].xcom_pull(key='csv_data', task_ids='read_csv')
    df4 = pd.read_json(df_json)
    df4 = df4.sort_values('Rating', ascending=False).head(5)
    df4.to_csv('/home/airflow/gcs/data/movies3.csv', index=False)
 
def transform_task(**kwargs):
    df_json = kwargs['ti'].xcom_pull(key='csv_data', task_ids='read_csv')
    df5 = pd.read_json(df_json)
    df5.to_csv('/home/airflow/gcs/data/movies4.csv', index=False)
 
def transform_least_duration_rating(**kwargs):
    df_json = kwargs['ti'].xcom_pull(key='csv_data', task_ids='read_csv')
    df6 = pd.read_json(df_json)
    df6 = df6[(df6['Duration'] < 150) & (df6['Rating'] < 5)].head(5)
    df6.to_csv('/home/airflow/gcs/data/movies5.csv', index=False)
 
def transform_genre_rating(**kwargs):
    df_json = kwargs['ti'].xcom_pull(key='csv_data', task_ids='read_csv')
    df7 = pd.read_json(df_json)
    df7 = df7[(df7['Genre'] == 'Action') & (df7['Rating'] == 10)].head(5)
    df7.to_csv('/home/airflow/gcs/data/movies6.csv', index=False)
 
read_csv_task = PythonOperator(
    task_id='read_csv',
    python_callable=read_csv,
    provide_context=True,
    dag=dag,
)
transform_data_task1 = PythonOperator(
    task_id='transform_check_genre',
    python_callable=transform_check_genre,
    provide_context=True,
    dag=dag,
)
transform_data_task2 = PythonOperator(
    task_id='transform_recent_releasedate',
    python_callable=transform_recent_releasedate,
    provide_context=True,
    dag=dag,
)
transform_data_task3 = PythonOperator(
    task_id='transform_top_duration',
    python_callable=transform_top_duration,
    provide_context=True,
    dag=dag,
)
transform_data_task4 = PythonOperator(
    task_id='transform_top_ratings',
    python_callable=transform_top_ratings,
    provide_context=True,
    dag=dag,
)
transform_data_task5 = PythonOperator(
    task_id='transform_task',
    python_callable=transform_task,
    provide_context=True,
    dag=dag,
)
transform_data_task6 = PythonOperator(
    task_id='transform_least_duration_rating',
    python_callable=transform_least_duration_rating,
    provide_context=True,
    dag=dag,
)
transform_data_task7 = PythonOperator(
    task_id='transform_genre_rating',
    python_callable=transform_genre_rating,
    provide_context=True,
    dag=dag,
)
 
read_csv_task >> transform_data_task1 >> transform_data_task2 >> transform_data_task3 >> transform_data_task4 >> transform_data_task5 >> transform_data_task6 >> transform_data_task7