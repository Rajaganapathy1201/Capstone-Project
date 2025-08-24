import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://root:Akshayaraj93#@localhost:3306/phonepe")
sdf = pd.read_sql("SELECT * FROM Agg_Trans", engine)
st.dataframe(sdf)