from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.operators.email import EmailOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='run_postgres_ingest_then_dbt',
    default_args=default_args,
    description='Ingest CSVs then run dbt models',
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

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command="""
        export PATH=$PATH:/home/airflow/.local/bin && \
        mkdir -p /tmp/dbt-logs && \
        export DBT_LOG_PATH=/tmp/dbt-logs && \
        cd /opt/airflow/dbt && dbt run --profiles-dir /opt/airflow/dbt
        """,
        env={
            'DBT_PROFILES_DIR': '/opt/airflow/dbt',
            'DBT_PROJECT_DIR': '/opt/airflow/dbt'
        },
        execution_timeout=timedelta(minutes=4),
    )

    run_dbt_tests = BashOperator(
        task_id='run_dbt_tests',
        bash_command='cd /opt/airflow/dbt && dbt test',
        execution_timeout=timedelta(minutes=3),
    )

    dbt_test_failed = EmailOperator(
        task_id='notify_dbt_test_failure',
        to='keyvan.tajbakhsh@gmail.com',
        subject='[Airflow] dbt test FAILED ❌',
        html_content="""
        <h3>dbt test step failed in DAG: run_postgres_ingest_then_dbt</h3>
        <p>Please investigate the issue.</p>
        """,
        trigger_rule='one_failed',
    )

    run_ingest >> run_dbt >> run_dbt_tests >> dbt_test_failed

