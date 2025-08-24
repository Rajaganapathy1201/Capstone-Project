from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:Akshayaraj93#@localhost:3306/phonepe")

import streamlit as st
import pandas as pd



# Top 5 states by total transaction amount
top_states = (
	Agg_Trans.groupby("State")["Transacion_amount"]
	.sum()
	.reset_index()
	.sort_values("Transacion_amount", ascending=False)
	.head(5)
	.rename(columns={"Transacion_amount": "total_amount"})
)

# Top 5 transaction types for a given year/quarter
year, quarter = 2023, 2
top_types = (
	Agg_Trans[(Agg_Trans["Year"] == str(year)) & (Agg_Trans["Quater"] == quarter)]
	.groupby("Transacion_type")["Transacion_amount"]
	.sum()
	.reset_index()
	.sort_values("Transacion_amount", ascending=False)
	.head(5)
	.rename(columns={"Transacion_amount": "total_amount"})
)

# Quarterly trend over time
trend = (
	Agg_Trans.groupby(["Year", "Quater"])["Transacion_amount"]
	.sum()
	.reset_index()
	.sort_values(["Year", "Quater"])
	.rename(columns={"Transacion_amount": "total_amount", "Quater": "quarter", "Year": "year"})
)
trend["period"] = trend.apply(lambda x: f"Q{x['quarter']}-{x['year']}", axis=1)

%pip install plotly

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import json

# Engine setup (as earlier)
# engine = create_engine(...)
# Use the existing 'engine' variable defined earlier in the notebook

st.title("PhonePe Transaction Insights")

# Sidebar filters
years = sorted(Agg_Trans["Year"].unique())
quarters = sorted(Agg_Trans["Quater"].unique())
sel_year = st.sidebar.selectbox("Year", years)
sel_quarter = st.sidebar.selectbox("Quarter", quarters)

# Filtered data using Agg_Trans DataFrame
state_df = (
    Agg_Trans[(Agg_Trans["Year"] == sel_year) & (Agg_Trans["Quater"] == sel_quarter)]
    .groupby("State")["Transacion_amount"]
    .sum()
    .reset_index()
    .sort_values("Transacion_amount", ascending=False)
    .rename(columns={"Transacion_amount": "total_amount", "State": "state"})
)

st.subheader(f"Top States — {sel_year} Q{sel_quarter}")
st.table(state_df.head())

fig = px.bar(state_df, x='state', y='total_amount', title="State-wise Totals")
st.plotly_chart(fig)

# Load India GeoJSON
geojson_path = "india_states.geojson"
if not os.path.exists(geojson_path):
    st.warning(f"GeoJSON file not found: {geojson_path}. Please provide the correct path or download the file.")
else:
    with open(geojson_path) as f:
        geo = json.load(f)

    st.subheader("India Map — Total Transaction Amount")
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
# Quarterly trend line using 'trend' DataFrame
trend_df = trend.copy()
st.subheader("Quarterly Total Trend")
st.line_chart(trend_df.set_index("period")["total_amount"])
st.line_chart(trend_df.set_index("period")["total_amount"])

tab1, tab2, tab3 = st.tabs(["Overview", "Top States", "Trends"])
with tab1:
    st.write("Your aggregated KPIs here...")
with tab2:
    st.bar_chart(state_df.set_index("state")["total_amount"])
with tab3:
    st.line_chart(trend_df.set_index("period")["total_amount"])

st.metric(label="Total Transactions", value="₹12.5 Cr", delta="+3% QOQ")

states = pd.read_sql("SELECT DISTINCT State FROM AGG_TRANS", engine)
selected_state = st.sidebar.selectbox("Select State", states['State'].tolist())
