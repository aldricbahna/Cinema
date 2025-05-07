import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data

df = load_data()

#st.set_page_config(layout="wide")
## df Acteurs

acteurs_series = df['Acteurs'].fillna('').str.split(',')
acteurs_flat = [acteur.strip() for sous_liste in acteurs_series for acteur in sous_liste if acteur]

acteur_counts = pd.Series(acteurs_flat).value_counts()
df_acteurs=acteur_counts.reset_index()
df_acteurs.columns=['Acteur','Nb_films']

df['Acteurs'] = df['Acteurs'].fillna('').str.split(',')

def moyenne_notes(acteur, df):
    notes = df[df['Acteurs'].apply(lambda x: acteur in [a.strip() for a in x])]['Note']
    return notes.mean()

df_acteurs['Moyenne_Notes'] = df_acteurs['Acteur'].apply(lambda x: moyenne_notes(x, df))

## Acteur spécifique

acteur_choisi=st.selectbox("Choisir un acteur",df_acteurs['Acteur'].unique())
dates=df[df['Acteurs'].apply(lambda x: acteur_choisi in [a.strip() for a in x])].index
df_dates = pd.DataFrame({'Date': dates, 'Occurrences': 1})

fig = px.bar(df_dates, x='Date', y='Occurrences', labels={'x': 'Date', 'y': 'Occurrences'},
             title=f"Périodes où j'ai vu un film de {acteur_choisi}", width=900, height=500)

fig.update_xaxes(range=[df.index.min(), date.today()])
fig.update_layout(bargap=1)

#st.plotly()

metric_moyenne=df[df['Acteurs'].apply(lambda x: acteur_choisi in [a.strip() for a in x])]['Note'].mean().round(1)
metric_std=df[df['Acteurs'].apply(lambda x: acteur_choisi in [a.strip() for a in x])]['Note'].std().round(1)
nom_films=df[df['Acteurs'].apply(lambda x: acteur_choisi in [a.strip() for a in x])][['Nom','Sortie','Sortie (France)','Note']]
nom_films.sort_index(ascending=False,inplace=True)

## df_acteur_choisi

df0 = load_data()
#fig2=px.box(data_frame=df_acteurs,x='Note')
df_acteur_choisi=df0[df0['Acteurs'].str.contains(acteur_choisi,case=False,na=False)]


fig2=px.box(data_frame=df_acteur_choisi,x='Note',range_x=[0, 11],width=900,height=300)

 

a,b=st.columns([3,2])
with a:
    st.plotly_chart(fig)
with b:
    st.metric("Moyenne",f"{metric_moyenne} ± {metric_std}")   
    st.dataframe(nom_films) 
st.plotly_chart(fig2)
    

st.dataframe(df_acteurs)