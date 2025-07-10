from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='run_postgres_ingest',
    default_args=default_args,
    description='Ingest CSVs',
    schedule_interval='*/5 * * * *',
    start_date=days_ago(1),
    catchup=False,
    is_paused_upon_creation=False,
    tags=['ingestion', 'dbt'],
) as dag:

    run_ingest = BashOperator(
        task_id='run_ingest_script',
        bash_command='python /opt/airflow/scripts/ingest_csv_files.py',
        execution_timeout=timedelta(minutes=4),
    )

