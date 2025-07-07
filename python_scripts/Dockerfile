FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .
