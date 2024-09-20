from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator

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
    dag_id='bq_to_gcs_load_dag',
    catchup=False,
    schedule_interval=timedelta(days=1),
    default_args=default_args
) as dag:

    # Dummy start task   
    start = DummyOperator(
        task_id='start'
    )

    # BigQuery to GCS data load Operator and task
    bq_to_gcs_load = BigQueryToGCSOperator(
        task_id='bq_to_gcs_load',
        source_project_dataset_table='customerp-1711290140039.sales_dataset.sales',
        destination_cloud_storage_uris=['gs://output-buc-001/sales.csv'],
        export_format='CSV',  # Format of the destination data
        force_rerun=True,  # Force rerun the job
        reattach_states=['DONE']  # Reattach to the job if it's in DONE state
    )

    # Dummy end task
    end = DummyOperator(
        task_id='end'
    )

    # Setting up task dependencies
    start >> bq_to_gcs_load >> end
