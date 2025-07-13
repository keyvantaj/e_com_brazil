FROM apache/airflow:2.7.3

USER root

# 1. Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        git \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN chown airflow: /tmp/requirements.txt

COPY dbt /opt/airflow/dbt
RUN chown -R airflow: /opt/airflow/dbt

# 4. Set PATH to include system Python binaries
ENV PATH="/usr/local/bin:${PATH}"

USER airflow

RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install --no-cache-dir \
    dbt-core==1.7.0 \
    dbt-postgres