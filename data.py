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
                   'Sortie France': 'Sortie (France)',
                   'Budget (M€)':'Budget euro',
                   'Budget (M$)':'Budget dollar',
                   'Box office France':'Box office fr',
                   'Nb Oscars':'Oscars',
                   'Nb nominations Oscars':'Nominations Oscars',
                   'Nb Césars':'Césars',
                   'Nb nominations César':'Nominations Césars',   
                   'MVP Aldric':'MVP'})
    
    def decennie(annee):
        if annee<1930:
            return "20's"
        elif annee<1940:
            return "30's"
        elif annee<1950:
            return "40's"
        elif annee<1960:
            return "50's"
        elif annee<1970:
            return "60's"
        elif annee<1980:
            return "70's"
        elif annee<1990:
            return "80's"
        elif annee<2000:
            return "90's"
        elif annee<2010:
            return "2000's"
        elif annee<2020:
            return "2010's"
        else:
            return "2020's"
    df['Décennie']=df['Sortie'].map(decennie)
    
    df_box_office=df[df['Box office fr']!='streaming']
    df['Pays']=df['Pays de production'].str.split(',').apply(lambda x: x[0].strip())
    df['Ciné num']=df['Ciné'].map(lambda x:1 if x=='oui' else 0)
    df['Box office fr (M)']=(df['Box office fr']/1000000).round(2)
    #df['Box office fr'] = pd.to_numeric(df['Box office fr'], errors='coerce')
    df['Letterbox']=df['Letterbox'].round(1)
    df['Sens Critique']=df['Sens Critique'].round(1)
    df['Année fr']=df['Sortie (France)'].dt.year
    df['Sortie (France)'] = pd.to_datetime(df['Sortie (France)'], errors='coerce')
    df['Sortie (France)'] = df['Sortie (France)'].dt.date
    df.index=df.index.date
    df['Sortie']=df['Sortie'].astype('str')

    dict_couleur={'Etats-Unis':'red',
                  'France':'mediumblue',
                  'Italie':'limegreen',
                  'Royaume-Uni':'lightblue',
                  'Hong Kong':'gold',
                  'Corée du Sud':'steelblue',
                  'Canada':'orangered',
                  'Japon':'pink',
                  'Allemagne':'orange',
                  "Allemagne de l'Ouest":'orange',
                  'Australie':'olivedrab',
                  'Suède':'yellow',
                  'Iran':'darkkhaki',
                  'URSS':'gainsboro'
                  }

    return df,dict_couleur
