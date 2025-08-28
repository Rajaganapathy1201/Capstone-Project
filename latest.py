import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import requests

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
engine = create_engine("mysql+pymysql://root:Vinayak12345@localhost:3306/phonepe")

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.title("📊 PhonePe Pulse Case Studies with Year & Quarter Filters")

# Sidebar filters
st.sidebar.header("🔎 Filters")

# Fetch distinct Year & Quarter from database
year_query = "SELECT DISTINCT Year FROM agg_trans ORDER BY Year;"
quarter_query = "SELECT DISTINCT Quarter FROM agg_trans ORDER BY Quarter;"

years = pd.read_sql(year_query, engine)["Year"].astype(str).tolist()
quarters = pd.read_sql(quarter_query, engine)["Quarter"].astype(int).tolist()

sel_year = st.sidebar.selectbox("Select Year", years)
sel_quarter = st.sidebar.selectbox("Select Quarter", quarters)

# Case study selector
case = st.selectbox("Choose a Case Study", [
    "Case 1: Transaction Count by State",
    "Case 2: Transaction Amount by State",
    "Case 3: Top 10 States by Transactions",
    "Case 4: Yearly Growth (Transactions)",
    "Case 5: Top Payment Types",
    "Case 6: Registered Users by State (Map)"
])

# -----------------------------
# CASE STUDY QUERIES WITH FILTERS
# -----------------------------

if case == "Case 1: Transaction Count by State":
    query = f"""
        SELECT State, SUM(Transacion_count) AS Total_Txn
        FROM agg_trans
        WHERE Year = '{sel_year}' AND Quarter = {sel_quarter}
        GROUP BY State;
    """
    df = pd.read_sql(query, engine)
    st.dataframe(df)
    st.plotly_chart(px.bar(df, x="State", y="Total_Txn",
                           title=f"Transactions by State ({sel_year} Q{sel_quarter})"))

elif case == "Case 2: Transaction Amount by State":
    query = f"""
        SELECT State, SUM(Transacion_amount) AS Total_Amount
        FROM agg_trans
        WHERE Year = '{sel_year}' AND Quarter = {sel_quarter}
        GROUP BY State;
    """
    df = pd.read_sql(query, engine)
    st.dataframe(df)
    st.plotly_chart(px.bar(df, x="State", y="Total_Amount",
                           title=f"Transaction Amount by State ({sel_year} Q{sel_quarter})"))

elif case == "Case 3: Top 10 States by Transactions":
    query = f"""
        SELECT State, SUM(Transaction_count) AS Total_Txn
        FROM Top_Trans_df
        WHERE Year = '{sel_year}' AND Quarter = {sel_quarter}
        GROUP BY State
        ORDER BY Total_Txn DESC
        LIMIT 10;
    """
    df = pd.read_sql(query, engine)
    st.dataframe(df)
    st.plotly_chart(px.pie(df, names="State", values="Total_Txn",
                           title=f"Top 10 States by Transactions ({sel_year} Q{sel_quarter})"))

elif case == "Case 4: Yearly Growth (Transactions)":
    query = f"""
        SELECT Year, SUM(Transacion_count) AS Total_Txn
        FROM agg_trans
        WHERE Year <= '{sel_year}'  -- show growth up to selected year
        GROUP BY Year
        ORDER BY Year;
    """
    df = pd.read_sql(query, engine)
    st.dataframe(df)
    st.plotly_chart(px.line(df, x="Year", y="Total_Txn", markers=True,
                            title=f"Yearly Growth of Transactions (Up to {sel_year})"))

elif case == "Case 5: Top Payment Types":
    query = f"""
        SELECT Transacion_type, SUM(Transacion_count) AS Total_Txn
        FROM agg_trans
        WHERE Year = '{sel_year}' AND Quarter = {sel_quarter}
        GROUP BY Transacion_type;
    """
    df = pd.read_sql(query, engine)
    st.dataframe(df)
    st.plotly_chart(px.bar(df, x="Transacion_type", y="Total_Txn",
                           title=f"Popular Payment Types ({sel_year} Q{sel_quarter})"))

elif case == "Case 6: Registered Users by State (Map)":
    query = f"""
        SELECT State, SUM(Registered_users) AS Total_Users
        FROM Top_User_df
        WHERE Year = '{sel_year}' AND Quarter = {sel_quarter}
        GROUP BY State;
    """
    df = pd.read_sql(query, engine)

    # Load India GeoJSON
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    india_states = requests.get(geojson_url).json()

    # Match state names with GeoJSON
    df["State"] = df["State"].str.title()

    st.dataframe(df)

    fig = px.choropleth(
        df,
        geojson=india_states,
        featureidkey="properties.ST_NM",
        locations="State",
        color="Total_Users",
        color_continuous_scale="Blues",
        title=f"Registered Users by State ({sel_year} Q{sel_quarter})"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)
