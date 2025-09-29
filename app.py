import streamlit as st
import pandas as pd
import psycopg2
import os

st.title("Brazil e-commerce Data Summary")

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=5432,
            dbname="olist",
            user="admin",
            password="admin"
        )
        return conn
    except Exception as e:
        st.error(f"Failed connect: {e}")
        return None
def load_data(query):
    try:
        conn = connect_to_db()
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

query = "SELECT * FROM analytics_analytics.fct_sales_by_product;"
df_sales = load_data(query)

if not df_sales.empty:
    st.subheader("📈 Sales by Product Category (from dbt)")
    st.dataframe(df_sales, use_container_width=True)
    st.bar_chart(df_sales.set_index("product_category_name")["total_sales"])

