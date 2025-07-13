from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 11),
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
    'max_active_runs': 1,
}

with DAG(
    'ecom_metrics',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
    tags=['ecommerce', 'metrics'],
) as dag:


    # Common environment variables for dbt
    dbt_env = {
        'DBT_PROFILES_DIR': '/opt/airflow/dbt',
        'PATH': '${PATH}:/home/airflow/.local/bin',
        'DBT_FULL_REFRESH': 'false',
    }

    # Run dbt transformations
    run_dbt = BashOperator(
        task_id='run_dbt_transform',
        bash_command=(
            'dbt run '
            '--project-dir /opt/airflow/dbt '
            '--profiles-dir /opt/airflow/dbt '
            '--select staging+ 2>&1'
        ),
        env=dbt_env,
        execution_timeout=timedelta(minutes=15)
    )

    # Run dbt tests
    test_dbt = BashOperator(
        task_id='run_dbt_tests',
        bash_command=(
            'dbt test '
            '--project-dir /opt/airflow/dbt '
            '--profiles-dir /opt/airflow/dbt '
            '--select staging+ 2>&1'
        ),
        env=dbt_env,
        execution_timeout=timedelta(minutes=15)
    )

    # Dependencies
    run_dbt >> test_dbt

    dag.doc_md = """
    ## E-commerce Metrics Pipeline
    Hourly DAG that:
    1. Installs dbt dependencies
    2. Runs dbt transformations on staging models
    3. Executes dbt data quality tests
    """