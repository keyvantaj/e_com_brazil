FROM apache/airflow:2.7.3

USER root

RUN if ! getent group airflow >/dev/null; then \
      groupadd -g 50000 airflow; \
    fi && \
    if ! id -u airflow >/dev/null 2>&1; then \
      useradd -u 50000 -g airflow airflow; \
    fi && \
    mkdir -p /opt/airflow/dbt && \
    chown -R airflow:airflow /opt/airflow

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=airflow:airflow requirements.txt /tmp/requirements.txt

USER airflow
WORKDIR /home/airflow

ENV PATH="$PATH:/home/airflow/.local/bin"

RUN pip install --no-cache-dir --user \
    dbt-core==1.6.0 \
    dbt-postgres==1.6.0

RUN pip install --no-cache-dir --user -r /tmp/requirements.txt

RUN python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__}')" && \
    python -c "import pandas; print(f'Pandas {pandas.__version__}')" && \
    (dbt --version || echo 'DBT sera installé via volume')