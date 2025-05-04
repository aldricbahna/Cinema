import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data

df = load_data()

decennie=st.selectbox("Choisissez une décennie", df['Décennie'].unique())
dfs=df[df['Décennie']==decennie]
fig_hist_notes_decennie=px.histogram(dfs,x='Note',nbins=100,title="Répartition des notes personnelles",labels={'Note': 'Note (sur 10)'},range_x=[0, 10.5],
                color_discrete_sequence=["blue"])


fig_hist_notes_decennie_euge=px.histogram(dfs,x='Eugénie',nbins=100,title="Répartition des notes d'Eugénie",labels={'Note': 'Note (sur 10)'},range_x=[0, 10.5],
                color_discrete_sequence=["pink"])

    
col1, col2 = st.columns(2)  
with col1:
    a,b=st.columns([3,1])
    with a:
        st.plotly_chart(fig_hist_notes_decennie)
    with b: 
        st.metric("Nombre :",f"{dfs['Note'].count()}")
        st.metric("Note moyenne :",f"{dfs['Note'].mean():.2f}")
        st.metric("Ecart-type :",f"{dfs['Note'].std():.2f}")
            
        
with col2:
    c,d=st.columns([3,1])
    with c:
        st.plotly_chart(fig_hist_notes_decennie_euge)
    with d: 
        st.metric("Nombre :",f"{dfs['Eugénie'].count()}")
        st.metric("Note moyenne :",f"{dfs['Eugénie'].mean():.2f}")
        st.metric("Ecart-type :",f"{dfs['Eugénie'].std():.2f}")

st.dataframe(dfs[['Nom','Année','Sortie fr','Réalisateur','Note','Eugénie','Durée','Acteurs']].sort_values(by='Sortie fr',ascending=False))