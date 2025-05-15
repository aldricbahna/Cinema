import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime,date, timedelta
from data import load_data

df,dict_couleur = load_data()

noms_films=df['Nom'].sort_values().unique().tolist()
nom_film = st.selectbox("Choisir un film", noms_films,index=noms_films.index('Le samouraï'))
dfs=df[df['Nom']==nom_film]

#st.write(dfs.loc(dfs.index,'Numéro jour'))
st.metric('Vu le', f"{dfs.iloc[0]['Numéro jour vu']}/{dfs.iloc[0]['Mois vu']:02d}/{int(dfs.iloc[0]['Année vu'])}")
st.metric("Note perso", dfs['Note'])
st.metric("Note Eugé", dfs['Eugénie'])
st.metric("Note Letterbox", dfs['Letterbox'])
st.metric("Note Sens Critique", dfs['Sens Critique'])

st.write("A compléter...")