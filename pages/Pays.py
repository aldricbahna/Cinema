import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data

df,dict_couleur = load_data()

fig_treemap_avec = px.treemap(df, path=['Pays'],color='Pays',color_discrete_map=dict_couleur,
                              title="Répartition des pays de production des films que j'ai vus")
st.plotly_chart(fig_treemap_avec)

pays_choisi=st.selectbox("Choisir un pays:", df['Pays'].unique())
dfs=df[df['Pays']==pays_choisi]

fig_hist_aldric = px.histogram(
        dfs,
        x='Note',               
        nbins=100,               
        title="Répartition des notes personnelles",
        labels={'Note': 'Note (sur 10)'},
        range_x=[0, 10.5],       
        color_discrete_sequence=["blue"], 
    )

fig_hist_euge = px.histogram(
        dfs,
        x='Eugénie',               
        nbins=100,               
        title="Répartition des notes d'Eugénie",
        labels={'Note': 'Note (sur 10)'},
        range_x=[0, 10.5],       
        color_discrete_sequence=["pink"], 
    )



col1, col2 = st.columns(2)  
with col1:
    a,b=st.columns([3,1])
    with a:
        st.plotly_chart(fig_hist_aldric)
    with b: 
        st.metric("Nombre :",f"{dfs['Note'].count()}")
        st.metric("Note moyenne :",f"{dfs['Note'].mean():.2f}")
        st.metric("Ecart-type :",f"{dfs['Note'].std():.2f}")
            
        
with col2:
    c,d=st.columns([3,1])
    with c:
        st.plotly_chart(fig_hist_euge)
    with d: 
        st.metric("Nombre :",f"{dfs['Eugénie'].count()}")
        st.metric("Note moyenne :",f"{dfs['Eugénie'].mean():.2f}")
        st.metric("Ecart-type :",f"{dfs['Eugénie'].std():.2f}")