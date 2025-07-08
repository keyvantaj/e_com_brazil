import pandas as pd
import os
from sqlalchemy import create_engine, text, MetaData
import sys
import warnings
from sqlalchemy.exc import SADeprecationWarning, OperationalError

warnings.filterwarnings("ignore", category=SADeprecationWarning)
# Load env vars
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "olist")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")
DB_ADMIN_PASS = os.getenv("DB_ADMIN_PASS", "admin")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, '/opt/airflow/data')

CSV_PATHS = {
    'products': (os.path.join(DATA_DIR, 'olist_products_dataset.csv'), 'product_id'),
    'sellers': (os.path.join(DATA_DIR, 'olist_sellers_dataset.csv'), 'seller_id'),
    'orders': (os.path.join(DATA_DIR, 'olist_orders_dataset.csv'), 'order_id'),
    'customers': (os.path.join(DATA_DIR, 'olist_customers_dataset.csv'), 'customer_id'),
    'order_items': (os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'), 'order_id'),
    'order_reviews': (os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'), 'review_id'),
    'order_payments': (os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv'), 'order_id'),
}

def load_data(file_path):
    try:
        df = pd.read_csv(file_path, low_memory=False)
        df = df.drop_duplicates(keep='first')
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df = df.replace('', None)
        df = df.loc[:, df.isnull().mean() < 0.8]
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load {file_path}: {e}")
        return None

def create_postgres_connection():
    try:
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        return engine
    except Exception as e:
        print(f"[ERROR] PostgreSQL connection failed: {e}")
        sys.exit(1)

def ensure_db_exists(db_name):
    """
    Ensures the target PostgreSQL database exists using SQLAlchemy.
    Requires admin access to connect to the 'postgres' system DB.
    """
    try:
        admin_engine = create_engine(
            f"postgresql://postgres:{DB_ADMIN_PASS}@{DB_HOST}:{DB_PORT}/postgres",
            isolation_level="AUTOCOMMIT"
        )
        with admin_engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db"),
                {"db": db_name}
            ).fetchone()

            if result is None:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"[INFO] Database '{db_name}' created.")
            else:
                print(f"[INFO] Database '{db_name}' already exists.")

        admin_engine.dispose()

    except OperationalError as e:
        print(f"[ERROR] Could not connect or create database '{db_name}': {e}")

def ensure_table_exists(df, table_name, engine):
    """
    Checks if a table exists in PostgreSQL. If it doesn't, creates it using df's schema.
    """
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)

        if table_name in metadata.tables:
            print(f"[INFO] Table '{table_name}' already exists.")
        else:
            print(f"[INFO] Table '{table_name}' does not exist. Creating...")
            df.head(0).to_sql(table_name, engine, index=False, if_exists="replace")  # creates schema only
            print(f"[INFO] Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to ensure table '{table_name}': {e}")

def copy_data_to_postgres(df, table_name, engine, key_id):
    try:
        with engine.connect() as conn:
            # Load existing keys
            existing_ids = pd.read_sql(f"SELECT DISTINCT {key_id} FROM {table_name}", conn)
            df = df[~df[key_id].isin(existing_ids[key_id])]

        if df.empty:
            print(f"[INFO] No new rows for {table_name}")
        else:
            df.to_sql(table_name, engine, index=False, if_exists="append")
            print(f"[INFO] Inserted {len(df)} new rows into {table_name}")
    except Exception as e:
        print(f"[ERROR] Failed to insert into {table_name}: {e}")

def get_removed_rows_from_csv(engine, df_csv, table_name, key_id):

    try:
        df_db = pd.read_sql(table_name, engine)

        # Ensure key column exists
        if key_id not in df_csv.columns or key_id not in df_db.columns:
            raise ValueError(f"Primary key '{key_id}' must exist in both CSV and DB.")

        # Compare primary key values
        removed_rows = df_db[~df_db[key_id].isin(df_csv[key_id])]
        return removed_rows

    except Exception as e:
        print(f"[ERROR] Could not compute removed rows for table '{table_name}': {e}")
        return pd.DataFrame()

def delete_rows_by_key(engine, table_name, df_rows, key_id):
    if df_rows.empty:
        return
    with engine.begin() as conn:
        for val in df_rows[key_id]:
            conn.execute(
                text(f"DELETE FROM {table_name} WHERE {key_id} = :id"),
                {"id": val}
            )

def main():

    print("------------------------------------------")
    print("------------------------------------------")
    print("[INFO] Starting ingestion job...")

    engine = create_postgres_connection()
    # ensure_db_exists(db_name='olist')
    # ensure_db_exists(db_name='dash')

    for table, value in CSV_PATHS.items():
        df = load_data(value[0])
        ensure_table_exists(df=df, table_name=table, engine=engine)

        if df is not None:
            copy_data_to_postgres(df=df, table_name=table, engine=engine, key_id=value[1])
            removed = get_removed_rows_from_csv(engine, df_csv=df, table_name=table, key_id=value[1])
            if not removed.empty:
                delete_rows_by_key(engine, table_name=table, df_rows=removed, key_id=value[1])
                print(f"[INFO] {len(removed)} rows removed from {table} since last load.")

            print("[INFO] Ingestion job completed.")
        else:
            print(f"[WARN] Skipping table {table} due to load failure.")
        print("------------------------------------------")
    engine.dispose()

if __name__ == "__main__":
    main()