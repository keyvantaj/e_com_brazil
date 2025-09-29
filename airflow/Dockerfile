FROM apache/airflow:2.7.3-python3.9

# Install dbt (core + postgres adapter) as airflow user
RUN pip install --user --no-cache-dir dbt-core dbt-postgres

USER root

RUN mkdir -p /opt/airflow/dbt_project/logs && \
    chown -R 50000:50000 /opt/airflow/dbt_project/logs
# (Optional) If you need system packages, you can temporarily switch to root
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/* \

USER airflow