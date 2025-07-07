import psycopg2

conn = psycopg2.connect(
    dbname="analytics",
    user="airflow",
    password="airflow",
    host="postgres",
    port=5432
)

cur = conn.cursor()
cur.execute("INSERT INTO my_table (col1) VALUES ('data from Python ETL');")
conn.commit()
cur.close()
conn.close()
