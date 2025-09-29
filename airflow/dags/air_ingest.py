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
    description='Ingest CSVs into Postgres then run dbt transformations',
    schedule_interval='*/5 * * * *',
    start_date=days_ago(1),
    catchup=False,
    is_paused_upon_creation=False,
    tags=['ingestion', 'dbt'],
) as dag:

    run_ingest = BashOperator(
        task_id='run_ingest_script',
        bash_command='python3 /opt/airflow/scripts/ingest_csv_files.py',
        execution_timeout=timedelta(minutes=4),
    )

    run_dbt = BashOperator(
        task_id='dbt_run',
        # safer: explicitly tell dbt where the project and profiles.yml are
        bash_command='dbt run --project-dir /opt/airflow/dbt_project --profiles-dir /opt/airflow/dbt_project',
        execution_timeout=timedelta(minutes=10),
    )

    run_ingest >> run_dbt

