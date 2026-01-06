import streamlit as st
import pandas as pd
import sqlite3
import os
from etl import run_etl

DB_PATH = "harvard_artifacts.db"

st.set_page_config(page_title="Harvard Artifacts Explorer", layout="wide")
st.title("Harvard Artifacts Data Explorer (ETL + SQL + Visualization)")

API_KEY = "1a7ae53e-a8d5-4ca8-8cbf-e12a843ceec9"

st.sidebar.header("Controls")

classification = st.sidebar.text_input("Enter Classification (e.g., Paintings, Coins)", "Paintings")
limit = st.sidebar.number_input("Number of Records to Fetch", min_value=50, max_value=3000, value=200)

if st.sidebar.button("Run ETL"):
    run_etl(classification, API_KEY, limit)
    st.sidebar.success("ETL completed!")

if st.sidebar.button("Show Metadata Table"):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM artifact_metadata LIMIT 300", conn)
    conn.close()
    st.dataframe(df)

st.header("SQL Query Runner")

query = st.text_area("Enter SQL Query:", "SELECT * FROM artifact_metadata LIMIT 20")

if st.button("Run Query"):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        st.dataframe(df)
        st.success(f"{len(df)} rows returned.")
    except Exception as e:
        st.error(str(e))

st.markdown("---")
st.caption("Built by Harikrishnan S · Powered by Harvard Art Museums API")
