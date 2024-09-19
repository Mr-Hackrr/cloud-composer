from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# Default arguments
default_args = {
    'start_date': datetime.combine(datetime.today() - timedelta(1), datetime.min.time()),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# DAG definition
with DAG(
    dag_id='gcs_to_bq_load_dag',
    catchup=False,
    schedule_interval=timedelta(days=1),
    default_args=default_args
) as dag:

    # Dummy start task   
    start = DummyOperator(
        task_id='start'
    )

    # GCS to BigQuery data load Operator and task
    gcs_to_bq_load = GCSToBigQueryOperator(
        task_id='gcs_to_bq_load',
        bucket='data_eng_demos0011', 
        source_objects=['sales.csv'], 
        destination_project_dataset_table='customerp-1711290140039.sales_dataset.sales', 

        skip_leading_rows=0,  
        source_format='CSV',  # Format of the source data
        create_disposition='CREATE_IF_NEEDED',  # Create the table if it doesn't exist
        write_disposition='WRITE_TRUNCATE',  # Overwrite the table if it already exists
    )

    # Dummy end task
    end = DummyOperator(
        task_id='end'
    )

    # Setting up task dependencies
    start >> gcs_to_bq_load >> end
