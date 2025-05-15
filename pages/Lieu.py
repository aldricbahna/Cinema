import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime,date, timedelta
from data import load_data

df,dict_couleur = load_data()

df_cine=df[df['Ciné'] =='oui']
on = st.toggle("Au ciné")

fig_treemap_lieu = px.treemap(df, path=['Visionnage'], title="Répartition des lieux où j'ai vu un film")
fig_treemap_lieu_cine = px.treemap(df_cine, path=['Visionnage'], title="Répartition des lieux où j'ai vu un film au ciné")
if on:
    st.plotly_chart(fig_treemap_lieu_cine)
else:
    st.plotly_chart(fig_treemap_lieu)

df_visionnage=df.groupby('Visionnage')['Note'].agg(Moyenne='mean',
                             Ecart_type='std',
Nombre='count')
df_visionnage['Moyenne']=df_visionnage['Moyenne'].round(2)
df_visionnage['Ecart_type']=df_visionnage['Ecart_type'].round(2)
df_visionnage_3=df_visionnage[df_visionnage['Nombre']>2]
df_visionnage_3=df_visionnage_3.sort_values(by='Moyenne',ascending=False)
#sns.boxplot(data=df,y=df['Visionnage'].unique(),x='Note')
a,b=st.columns([1.5,3])
with a:
    st.dataframe(df_visionnage_3)
with b:
    index_christine=df['Visionnage'].unique().tolist().index('Christine')
    lieu=st.selectbox("Choisir un lieu", df['Visionnage'].unique(),index=index_christine)
    df_lieu=df[df['Visionnage']==lieu]
    st.dataframe(df_lieu[['Nom','Sortie','Note','Eugénie','MVP','Letterbox']].sort_index(ascending=False))