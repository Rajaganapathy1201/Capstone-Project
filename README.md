**Files relevant to this project :**
1. README.md
2. extraction.ipynb
3. latest.py


📊 **PhonePe Pulse – Streamlit + MySQL Project**
📌 **Overview:**

This project is a beginner-friendly data visualization web app built with Streamlit and connected to a MySQL database containing PhonePe Pulse data.

The app allows users to explore digital payment transactions across Indian states with:

Interactive charts

Dynamic filters (Year & Quarter)

SQL-powered queries

Choropleth map of registered users

This project is ideal for students, beginners, and analysts who want to learn how to combine Python, MySQL, and Streamlit for data-driven dashboards.

✨ **Features**

🔗 MySQL + Streamlit integration (via SQLAlchemy)

📈 Interactive visualizations using Plotly (bar, line, pie, and maps)

🧮 SQL-driven queries for real-time insights

🧭 Sidebar filters for Year and Quarter selections

🌍 Choropleth Map of India showing registered users by state

📚 **Covers 6 Case Studies:**

    1. Transaction Count by State

    2. Transaction Amount by State

    3. Top 10 States by Transactions

    4. Yearly Growth (Transactions)

    5. Top Payment Types

    6. Registered Users by State (Map)
    

🗂 **Dataset & Database**

The PhonePe dataset is assumed to be stored in MySQL with the following tables:

agg_trans → Aggregated transactions (state, year, quarter, count, amount, type)

top_trans_df → Top states/districts by transaction count

top_user → Registered users across states



🛠 **Requirements**

Python 3.x

MySQL Server (with PhonePe dataset loaded)

Python Libraries:

streamlit → for web app

pandas → for data handling

sqlalchemy & pymysql → MySQL connection

plotly → interactive charts

requests → fetch India GeoJSON for map

reportlab → export reports (optional)

Install dependencies:

pip install streamlit pandas sqlalchemy pymysql plotly requests reportlab


🚀 **How to Run**

1. Clone/download the project folder

2. Ensure MySQL server is running and PhonePe tables are created.

3. Update MySQL credentials

engine = create_engine("mysql+pymysql://username:password@localhost:3306/phonepe")

4. Ensure Sql queries are created and Stream lit codes are done.
   
5. Run the Streamlit app

6. The app will open at: http://localhost:8501
   

📊 **Output Snapshots**

📍 Bar chart: Transactions by State

📍 Line chart: Yearly growth trends

📍 Pie chart: Top 10 states by transactions

📍 Choropleth Map: Registered Users by State

🎯 Learning Outcomes

**Learnings from this project:**

1. How to connect Streamlit with MySQL

2. How to write SQL queries for analytics

3. How to use Plotly for interactive data visualization

4. How to implement India maps(2d) with GeoJSON

5. How to structure a beginner-friendly data project

👨‍💻 Author

Your Name
📧 rgpathy@outlook.com

🌐 https://github.com/Rajaganapathy1201/Capstone-Project.git
