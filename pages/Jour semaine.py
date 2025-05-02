import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data


df = load_data()

jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
min_date = df.index.min().to_pydatetime() # pour convertir de datetime64[ns] à datetime.datetime nécessaire pour les slider
max_date = df.index.max().to_pydatetime()
ajd = datetime.now()
ajd=ajd.replace(hour=0, minute=0, second=0, microsecond=0)

debut_charbon=datetime(2023,11,1,0,0) #une autre façon plutôt que de passer par pd.datetime() puis convertir en datime.datetime
periode = st.sidebar.slider(
                "Période:",
                min_value=min_date,
                max_value=max_date,
                value=(debut_charbon, ajd),
                format="YYYY-MM-DD"  
        )


dfs = df[(df.index >= periode[0]) & (df.index <= periode[1])]

df_jour_semaine=dfs.groupby('Jour semaine')['Nom'].count().reset_index()
df_jour_semaine.rename(columns={'Nom':'Nombre'},inplace=True)
#df_jour_semaine['Jour semaine'] = pd.Categorical(df_jour_semaine['Jour semaine'], categories=jours_semaine_ordre,ordered=True)  
fig_bar_jour_semaine=px.bar(df_jour_semaine,x='Jour semaine',y='Nombre',category_orders={'Jour semaine':jours_semaine_ordre})
st.plotly_chart(fig_bar_jour_semaine)

df2=dfs[dfs.index>'2023-11-01']
st.dataframe(df2)

jours_semaine = {
    "lundi": 0,
    "mardi": 0,
    "mercredi": 0,
    "jeudi": 0,
    "vendredi": 0,
    "samedi": 0,
    "dimanche": 0
}

current_date = debut_charbon
while current_date <= ajd:
    # Obtenir le jour de la semaine (0 = lundi, 1 = mardi, ..., 6 = dimanche)
    if current_date.weekday() == 0:
        jours_semaine["lundi"] += 1
    elif current_date.weekday() == 1:
        jours_semaine["mardi"] += 1
    elif current_date.weekday() == 2:
        jours_semaine["mercredi"] += 1
    elif current_date.weekday() == 3:
        jours_semaine["jeudi"] += 1
    elif current_date.weekday() == 4:
        jours_semaine["vendredi"] += 1
    elif current_date.weekday() == 5:
        jours_semaine["samedi"] += 1
    elif current_date.weekday() == 6:
        jours_semaine["dimanche"] += 1
    
    current_date += timedelta(days=1)
    


df_jour_semaine['Nombre écoulé']=0
df_jour_semaine.set_index('Jour semaine',inplace=True)

# Afficher le nombre de chaque jour
for jour, count in jours_semaine.items():
    df_jour_semaine.loc[jour,'Nombre écoulé']=count

df_jour_semaine['% Jour semaine']=df_jour_semaine['Nombre']/df_jour_semaine['Nombre écoulé']*100
st.write(df_jour_semaine)

fig_bar_jour_semaine_pourcentage=px.bar(df_jour_semaine,x=df_jour_semaine.index,y='% Jour semaine',category_orders={'Jour semaine':jours_semaine_ordre})
st.plotly_chart(fig_bar_jour_semaine_pourcentage)