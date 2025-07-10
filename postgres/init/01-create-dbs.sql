-- Créer la DB olist si elle n'existe pas
SELECT 'CREATE DATABASE olist' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'olist')\gexec

-- Créer la DB airflow_meta si elle n'existe pas
SELECT 'CREATE DATABASE airflow_meta' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow_meta')\gexec

-- Créer la DB dbt if elle n'existe pas
SELECT 'CREATE DATABASE dash'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dash')\gexec