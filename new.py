import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import json
import os

# Connect to MySQL database
engine = create_engine("mysql+pymysql://root:Vinayak12345@localhost:3306/phonepe")

st.title("📊 PhonePe Insights Dashboard")

# Sidebar: Table Selection
table_option = st.sidebar.selectbox("Select Data Table", ["Agg_Trans", "User_Device_df"])

# Load data based on selected table
if table_option == "Agg_Trans":
    df = pd.read_sql("SELECT * FROM agg_trans", engine)
    df.columns = df.columns.str.strip()  # Remove any whitespace in column names
    df['Year'] = df['Year'].astype(str)
    df['Quarter'] = df['Quarter'].astype(int)  # corrected 'Quater' to 'Quarter'

    # Sidebar filters
    years = sorted(df["Year"].unique())
    quarters = sorted(df["Quarter"].unique())
    sel_year = st.sidebar.selectbox("Select Year", years)
    sel_quarter = st.sidebar.selectbox("Select Quarter", quarters)

    # Filtered data
    filtered_df = df[(df["Year"] == sel_year) & (df["Quarter"] == sel_quarter)]

    st.subheader(f"📄 Transactions — {sel_year} Q{sel_quarter}")
    st.dataframe(filtered_df)

    # State-wise totals
    state_query = f"""
    SELECT 
        State AS state,
        SUM(Transacion_amount) AS total_amount
    FROM 
        agg_trans
    WHERE 
        Year = '{sel_year}' AND Quarter = {sel_quarter}
    GROUP BY 
        State
    ORDER BY 
        total_amount DESC;
    """
    state_df = pd.read_sql(state_query, engine)

    st.subheader(f"🏆 Top States — {sel_year} Q{sel_quarter}")
    st.table(state_df.head())

    fig = px.bar(state_df, x='state', y='total_amount', title="State-wise Transaction Totals")
    st.plotly_chart(fig)

    # Choropleth map
    geojson_path = "india_states.geojson"
    if not os.path.exists(geojson_path):
        st.warning("GeoJSON file not found. Map can't be displayed.")
    else:
        with open(geojson_path) as f:
            geo = json.load(f)

        st.subheader("🗺️ India Map — Transaction Amount by State")
        fig2 = px.choropleth(
            state_df,
            geojson=geo,
            locations="state",
            featureidkey="properties.ST_NM",
            color="total_amount",
            color_continuous_scale="Viridis"
        )
        fig2.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig2)

elif table_option == "User_Device_df":
    df = pd.read_sql("SELECT * FROM User_Device_df", engine)
    df.columns = df.columns.str.strip()
    df['Year'] = df['Year'].astype(str)
    df['Quarter'] = df['Quarter'].astype(int)

    # Sidebar filters
    years = sorted(df["Year"].unique())
    quarters = sorted(df["Quarter"].unique())
    sel_year = st.sidebar.selectbox("Select Year", years)
    sel_quarter = st.sidebar.selectbox("Select Quarter", quarters)

    # Filtered data
    filtered_df = df[(df["Year"] == sel_year) & (df["Quarter"] == sel_quarter)]

    st.subheader(f"📱 Device Users — {sel_year} Q{sel_quarter}")
    st.dataframe(filtered_df)

    # Brand-wise user count
    query2 = f"""
    SELECT 
        Device_Brand,
        SUM(User_Count) AS total_users
    FROM 
        User_Device_df
    WHERE 
        Year = '{sel_year}' AND Quarter = {sel_quarter}
    GROUP BY 
        Device_Brand
    ORDER BY 
        total_users DESC;
    """           
    brand_df = pd.read_sql(query2, engine)

    st.subheader("📱 Top Device Brands")
    st.table(brand_df.head())

    fig = px.bar(brand_df, x="Device_Brand", y="total_users", title="Users by Device Brand")
    st.plotly_chart(fig)

# Footer metric
st.metric(label="📈 Insights Loaded", value="Success ✅")
