import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime,date, timedelta
from data import load_data

df = load_data()

annees=[i for i in range(1937,2027)]
df_annees = pd.DataFrame(annees, columns=['Sortie'])
df_annees['Sortie']=df_annees['Sortie'].astype('str')

df_annees_films=df.groupby('Sortie')['Nom'].count().reset_index()

df_annees=pd.merge(df_annees,df_annees_films,on='Sortie',how='left')
df_annees.replace(np.nan,0,inplace=True)


fig_bar_sortie_annees=px.bar(df_annees,x='Sortie',y='Nom')
tickvals=[i for i in range(1940,2026,5)]
fig_bar_sortie_annees.update_layout(xaxis=dict(tickvals=tickvals))


st.plotly_chart(fig_bar_sortie_annees)

title = st.text_input("Année", "1967")

df_annee_affiche=df[df['Sortie']==title]
a,b=st.columns([4,1])
with a:
    st.dataframe(df_annee_affiche[['Nom','Sortie (France)','Réalisateur','Note','Durée','Acteurs']].sort_index(ascending=False))
with b:
    c,d=st.columns(2)
    with d:
        if df_annee_affiche.shape[0]>0:
            if df_annee_affiche.shape[0]==1:
                st.metric("Note moyenne",f"{df_annee_affiche['Note'].mean().round(1)}")
            else:
                st.metric("Note moyenne",f"{df_annee_affiche['Note'].mean().round(1)} ± {df_annee_affiche['Note'].std().round(1)}")
