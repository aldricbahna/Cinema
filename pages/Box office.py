import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data
import numpy as np

st.subheader("Avec du web-scraping, quelques infos intéressantes sur les films que j'ai vus")
df,dict_couleur = load_data()
df_scrap=pd.read_excel("BDD_scraping_ajout_fonctions.xlsx",index_col='Vu le', parse_dates=True)
df_scrap.index=df_scrap.index.date
df_scrap.reset_index(inplace=True)
df.reset_index(inplace=True)
df_scrap=pd.merge(df_scrap,df,on=['index','Nom'],how='left')
df_scrap.set_index('index',inplace=True)
df_scrap['ENTREES PARIS']=df_scrap['ENTREES PARIS'].replace(0,np.nan)


df_scrap.replace('-$',np.nan,inplace=True)
df_scrap.replace('-',np.nan,inplace=True)
#df_scrap.replace('$','',inplace=True)
df_scrap[df_scrap.columns[1:6]] = df_scrap[df_scrap.columns[1:6]].apply(lambda x: x.str.replace(r'\$', '', regex=True) if x.dtype == "object" else x)
df_scrap['Rentabilité France']=df_scrap['Rentabilité France'].astype(str).str.replace(r'%', '', regex=True)

for col in df_scrap.columns[1:10]:
    df_scrap[col] = pd.to_numeric(df_scrap[col], errors='coerce')




df_scrap['Entrées/démarrage']=df_scrap['ENTREES']/df_scrap['DEMARRAGE']
df_scrap['Ratio entrées France/Paris']=df_scrap['ENTREES']/df_scrap['ENTREES PARIS']
df_scrap['Ratio entrées Paris/France']=df_scrap['ENTREES PARIS']/df_scrap['ENTREES']

n_bars=40
## Entrées France
df_box_office_fr=df_scrap.sort_values('ENTREES',ascending=False)
fig_bar_films_entree_fr=px.bar(data_frame=df_box_office_fr.head(n_bars),x='Nom',y='ENTREES',color='Pays',category_orders={'Nom': df_box_office_fr['Nom'].tolist()},color_discrete_map=dict_couleur,
                               title="Parmi les films que j'ai vus, les 40 films qui ont fait le plus d'entrées en France")
st.plotly_chart(fig_bar_films_entree_fr)

## Ratio Entrées Démarrage

df_ratio_entrees_demarrage_fr=df_scrap.sort_values('Entrées/démarrage',ascending=False)
fig_bar_films_ratio_entrees_demarrage_fr=px.bar(data_frame=df_ratio_entrees_demarrage_fr.head(n_bars),x='Nom',y='Entrées/démarrage',color='Pays',category_orders={'Nom': df_ratio_entrees_demarrage_fr['Nom'].tolist()},color_discrete_map=dict_couleur,
                                                title="Films dont le ratio Nombre d'entrée final en France / Démarrage 1ère semaine sont les plus élevés -> très bon bouche à oreille et critiques")
st.plotly_chart(fig_bar_films_ratio_entrees_demarrage_fr)

df_ratio_entrees_demarrage_negatif_fr=df_scrap.sort_values('Entrées/démarrage')
fig_bar_films_ratio_entrees_demarrage_negatif_fr=px.bar(data_frame=df_ratio_entrees_demarrage_negatif_fr.head(n_bars),x='Nom',y='Entrées/démarrage',color='Pays',category_orders={'Nom': df_ratio_entrees_demarrage_negatif_fr['Nom'].tolist()},color_discrete_map=dict_couleur,
                                                        title="Films dont le ratio Nombre d'entrée final en France / Démarrage 1ère semaine sont les plus faibles -> peu de bouche à oreille et/ou mauvaises critiques")
st.plotly_chart(fig_bar_films_ratio_entrees_demarrage_negatif_fr)

## Ratio France Paris

df_ratio_entrees_france_paris=df_scrap.sort_values('Ratio entrées France/Paris',ascending=False)
fig_bar_entrees_france_paris=px.bar(data_frame=df_ratio_entrees_france_paris.head(n_bars),x='Nom',y='Ratio entrées France/Paris',color='Pays',category_orders={'Nom': df_ratio_entrees_france_paris['Nom'].tolist()},color_discrete_map=dict_couleur,
                                    title="Films ayant le plus marché en 'province' -> sur 17 personnes qui sont allés voir 'Une vie', seulement 1 personne était parisienne")
st.plotly_chart(fig_bar_entrees_france_paris)

df_ratio_entrees_paris_france=df_scrap.sort_values('Ratio entrées Paris/France',ascending=False)
fig_bar_entrees_paris_france=px.bar(data_frame=df_ratio_entrees_paris_france.head(n_bars),x='Nom',y='Ratio entrées Paris/France',color='Pays',category_orders={'Nom': df_ratio_entrees_paris_france['Nom'].tolist()},color_discrete_map=dict_couleur,
                                    title="Films ayant le plus marché à Paris -> 60% des français qui sont allés voir 'La grande belleza' étaient parisiens" )
st.plotly_chart(fig_bar_entrees_paris_france)

st.write("Comme on pouvait s'en douter, les films français marchent mieux en province qu'à Paris")


## BOX OFFICE US

df_box_office_us=df_scrap.sort_values('Box office USA',ascending=False)
fig_bar_us=px.bar(data_frame=df_box_office_us.head(40),x='Nom',y='Box office USA',color='Pays',category_orders={'Nom': df_box_office_us['Nom'].tolist()},color_discrete_map=dict_couleur,
                  title="Parmi les films que j'ai vus, les 40 films qui ont le box office américain le plus élevé (en $)")
st.plotly_chart(fig_bar_us)

fig_scatter_entrees_note=px.density_heatmap(df_scrap,x='Note',y='ENTREES',
                                            title="Nombre d'entrées en France vs Notes que j'ai attribué aux différents films")
st.plotly_chart(fig_scatter_entrees_note)
