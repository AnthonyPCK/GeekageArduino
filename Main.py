
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
#df["Time"] = df.Date.values.astype(np.int64) // 10 ** 9
df["diffTime"] = np.concatenate((np.array([0]),np.diff((df.Date.values.astype(np.int64) // 10 ** 9)/60/60)))

ParamPerte = 0.024 # °C/h/°C
ParamChauffPassive = 0.08 # °C/h (appareils elec + chaleur humaine + UV-IR)
for ii in df.index:
    if ii>1:
        df.at[ii,"Modele_StationCh"] = df.at[ii-1,"Modele_StationCh"] + ((df.at[ii,"TempStationChaptuzat"]-df.at[ii-1,"Modele_StationCh"])*ParamPerte + ParamChauffPassive)*df.at[ii,"diffTime"]
        df.at[ii,"Modele_MeteoOWM"] = df.at[ii-1,"Modele_MeteoOWM"] + ((df.at[ii,"TempOWM"]-df.at[ii-1,"Modele_MeteoOWM"])*ParamPerte + ParamChauffPassive)*df.at[ii,"diffTime"]
        Tint = df.at[ii,"TempInt"]
        Text = df.at[ii,"TempStationChaptuzat"]
        Text2 = df.at[ii,"TempOWM"]

st.write('Temperature intérieure = ', Tint)
st.write('Temperature extérieure Chap = ', Text)
st.write('Temperature extérieure OWM = ', Text2)


Voies = ['Date', 'TempInt', "TempStationChaptuzat", 'Modele_StationCh', 'TempOWM', 'Modele_MeteoOWM']
df2=df[Voies].tail(4500)
fig0 = px.line(df2, x=df2.Date, y=df2.columns,title="Derniers jours :")
st.plotly_chart(fig0, use_container_width=True)  

Voies = ['Date', 'TempInt', "TempStationChaptuzat", 'Modele_StationCh', 'Modele_MeteoOWM']
df3=df[Voies]
fig1 = px.line(df3, x=df3.Date, y=df3.columns,title="Modélisation :")
st.plotly_chart(fig1, use_container_width=True)  

fig2 = px.line(df, x=df.Date, y=df.columns,range_y=[-20, 100],title="Tout :")
st.plotly_chart(fig2, use_container_width=True)  

fig3 = px.scatter(df, x=df.Date, y=df.columns,title="Tout :")
st.plotly_chart(fig3, use_container_width=True)  
