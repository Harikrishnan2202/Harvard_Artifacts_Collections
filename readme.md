Harvard Artifacts Collections – ETL + SQL + Streamlit
A full-stack data engineering and visualization project that fetches artifact data, processes it through an ETL pipeline, stores it in a database, and presents insights using an interactive Streamlit web application.

---

## 🚀 Features
- Automated data fetching from external sources
- ETL pipeline for cleaning and transforming data
- Database storage using SQLAlchemy
- Interactive web dashboard built with Streamlit
- Scalable and modular project structure

---

## 🛠️ Tech Stack
- Python
- Streamlit
- Pandas
- SQLAlchemy
- SQLite
- Requests
- Altair

---
This project extracts data from the Harvard Art Museums API, stores it in a SQLite database, and provides a Streamlit dashboard for data viewing and SQL queries.

✅ Project Files

db.py → Creates SQLite tables

etl.py → Fetches API data and inserts into DB

app.py → Streamlit dashboard

requirements.txt → Python libraries

🔧 Setup Steps
1. Create Virtual Environment
python -m venv venv

2. Activate Environment

Windows:

venv\Scripts\activate

3. Install Libraries
pip install -r requirements.txt

4. Initialize Database
python dp.py

5. Add Your API Key

Inside etl.py and app.py:

API_KEY = "your_api_key_here"

🚀 Run ETL (Download & Store Data)
python etl.py

📊 Run Streamlit Dashboard
streamlit run app.py


Then open:

http://localhost:8501

🧪 Use the Dashboard

Enter a classification (ex: Paintings, Coins)

Run ETL

View metadata

Run SQL queries