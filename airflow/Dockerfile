FROM apache/airflow:2.7.3

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=airflow:airflow requirements.txt /tmp/requirements.txt

USER airflow
WORKDIR /home/airflow

ENV PATH="$PATH:/home/airflow/.local/bin"

RUN pip install --no-cache-dir --user -r /tmp/requirements.txt