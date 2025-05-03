import pandas as pd
import streamlit as st


@st.cache_data #Important !! à revoir
def load_data():
    df = pd.read_excel("BDD_FILMS.xlsx", index_col='Vu le', parse_dates=True)
    df['Nom'] = df['Nom'].astype(str)
    df['Sortie France'] = pd.to_datetime(df['Sortie France'])
    df['Jour semaine'] = df.index.strftime('%A')
    df['Numéro semaine']=df.index.isocalendar().week
    df['Numéro jour vu']=df.index.day
    df['Mois vu']=df.index.month
    df['Année vu']=df.index.year
    jours = {
        'Monday': 'lundi',
        'Tuesday': 'mardi',
        'Wednesday': 'mercredi',
        'Thursday': 'jeudi',
        'Friday': 'vendredi',
        'Saturday': 'samedi',
        'Sunday': 'dimanche'
        }

    df['Jour semaine'] = df['Jour semaine'].map(jours)

    df=df.rename(columns={'Note à froid':'Note',
                   "Sortie pays":'Sortie',
                   'Sortie France': 'Sortie fr',
                   'Pays de production':'Pays',
                   'Budget (M€)':'Budget euro',
                   'Budget (M$)':'Budget dollar',
                   'Box office France':'Box office fr',
                   'Nb Oscars':'Oscars',
                   'Nb nominations Oscars':'Nominations Oscars',
                   'Nb Césars':'Césars',
                   'Nb nominations César':'Nominations Césars',   
                   'MVP Aldric':'MVP'})
    df_box_office=df[df['Box office fr']!='streaming']
    df['Ciné num']=df['Ciné'].map(lambda x:1 if x=='oui' else 0)
    df['Box office fr (M)']=(df['Box office fr']/1000000).round(2)
    #df['Box office fr'] = pd.to_numeric(df['Box office fr'], errors='coerce')
    df['Letterbox']=df['Letterbox'].round(1)
    df['Sens Critique']=df['Sens Critique'].round(1)
    df['Année']=df['Sortie fr'].dt.year
    df['Sortie fr'] = pd.to_datetime(df['Sortie fr'], errors='coerce')
    df['Sortie fr'] = df['Sortie fr'].dt.date
    df['Sortie']=df['Sortie'].astype('str')
    return df
