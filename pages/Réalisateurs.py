import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data


df = load_data()

onglet = st.sidebar.radio(
    "Sous-onglets",
    ["Individuel", "Global"],
    index=0)


## df Réalisateurs

df_realisateurs=df.groupby('Réalisateur').agg(
    Nombre=('Nom','nunique'),
    Moyenne=('Note','mean'),
    Ecart_type=('Note','std')).reset_index().round({'Moyenne': 2, 'Ecart_type': 2})
df_realisateurs.sort_values('Nombre',ascending=False,inplace=True)
df_realisateurs.set_index('Réalisateur',inplace=True)
realisateurs=df_realisateurs.index

if onglet=='Global':
    st.dataframe(df_realisateurs)

else:

## Réalisateur choisi

    real_choisi=st.selectbox("Choisis un réalisateur : ",realisateurs)

    df_real_choisi=df[df['Réalisateur']==real_choisi]
    #st.dataframe(df_real_choisi)


    moyenne=df_real_choisi['Note'].mean().round(1)
    std=df_real_choisi['Note'].std().round(1)

    moyenne_lb=df_real_choisi['Letterbox'].mean().round(1)
    std_lb=df_real_choisi['Letterbox'].std().round(1)

    moyenne_sens_critique=df_real_choisi['Sens Critique'].mean().round(1)
    std_sens_critique=df_real_choisi['Sens Critique'].std().round(1)

    fig_occurence=px.bar(data_frame=df_real_choisi,x=df_real_choisi.index)
    fig_occurence.update_xaxes(range=[df.index.min(), date.today()],title_text='')
    fig_occurence.update_yaxes(dtick=1)
    fig_occurence.update_layout(title={
        'text': "Visionnage",
        'x': 0.5
        },bargap=1)

    df_real_choisi.sort_index(ascending=False,inplace=True)

    fig_pie=px.pie(df_real_choisi,'Genre principal')

    df_real_choisi_sortie=df_real_choisi.sort_values('Sortie fr')
    st.write(df_real_choisi_sortie.dtypes)
    fig_sortie=px.bar(df_real_choisi_sortie,x='Sortie fr',height=400)
    fig_sortie.update_yaxes(dtick=1)
    fig_sortie.update_xaxes(range=[df['Sortie'].min(), date.today()],title_text='')
    fig_sortie.update_layout(title={
        'text': "Sortie",
        'x': 0.5
        },bargap=1)

    a,b=st.columns([3.2,1.8])
    with a:
        st.plotly_chart(fig_occurence)
        st.plotly_chart(fig_sortie)
    with b:
        c,d,e=st.columns(3)
        with c:
            st.metric("Perso",f"{moyenne} ± {std}")
        with d:
            st.metric("Letterbox",f"{moyenne_lb} ± {std_lb}")
        with e :
            st.metric("Sens Critique",f"{moyenne_sens_critique} ± {std_sens_critique}")
        st.dataframe(df_real_choisi[['Nom','Sortie','Note','Eugénie','MVP']])
        st.plotly_chart(fig_pie)







