
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 11:05:36 2023

@author: antho
"""

#%reset -f
#%clear

import streamlit as st
from sqlite3 import connect
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.offline import plot
import plotly.graph_objects as go
import pathlib
import uuid
from scipy.optimize import least_squares

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])
df.Date = pd.to_datetime(df.Date)
df["Time"] = df.Date.to_timestamp
# Print results.
#for row in df.itertuples():
#    st.write(f"{row.Time}")



#df["diffTime"] = np.concatenate((np.array([0]),np.diff(df.Date)))
#for row in df.itertuples():
#    st.write(f"{row.diffTime}")

Voies = ['Date', 'TempInt', 'Modele_StationCh', 'Modele_MeteoOWM']
df2=df[Voies]
fig1 = px.scatter(df2, x=df2.Date, y=df2.columns,title="Modélisation :")
st.plotly_chart(fig1, use_container_width=True)  


fig2 = px.scatter(df, x=df.Date, y=df.columns,range_y=[-20, 100],title="Tout :")
st.plotly_chart(fig2, use_container_width=True)  

fig3 = px.scatter(df, x=df.Date, y=df.columns,title="Tout :")
st.plotly_chart(fig3, use_container_width=True)  
