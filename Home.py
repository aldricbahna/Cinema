import streamlit as st
from data import load_data
import plotly.express as px
from datetime import datetime,date, timedelta
import pandas as pd
st.set_page_config(layout="wide")

df,dict_couleur = load_data()
df.index = pd.to_datetime(df.index)

if df is not None:
    a0,b0=st.columns([4,1])
    with a0:
        st.title(f"Bienvenue dans ma mini wep-app Cinéma")
    with b0:
        st.metric("Nombre films vus", df.shape[0])
    st.subheader("N'hésitez pas à dezoomer et à mettre en plein écran pour plus de lisibilté")

    jours_semaine_ordre = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    min_date = df.index.min() # pour convertir de datetime64[ns] à datetime.datetime nécessaire pour les slider
    max_date = df.index.max()
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
    dfs['Nb films vus'] = range(1, len(dfs) + 1)

    fig_line=px.line(dfs['Nb films vus'],title='Evolution du nombre de films vus en fonction du temps')

    fig_pie=px.pie(dfs,'Ciné',title="Vu au cinéma ?",color='Ciné',
        color_discrete_map={
            'non': 'purple',
            'oui': 'red'
        })

    fig_treemap_avec = px.treemap(dfs, path=['Avec'], title="Vu avec ...")

    df_jour_semaine=dfs.groupby('Jour semaine')['Note'].agg(
        Nombre='count',
        Moyenne='mean',
        ).reset_index()
    df_cine_somme=dfs.groupby('Jour semaine')['Ciné num'].sum().reset_index()
    df_jour_semaine=pd.merge(df_jour_semaine,df_cine_somme,on='Jour semaine',how='left')
    #df_jour_semaine['Jour semaine'] = pd.Categorical(df_jour_semaine['Jour semaine'], categories=jours_semaine_ordre,ordered=True) 

    fig_bar_jour_semaine=px.bar(df_jour_semaine,x='Jour semaine',y='Nombre',category_orders={'Jour semaine':jours_semaine_ordre})

    #df2=dfs[dfs.index>'2023-11-01']

    jours_semaine = {
        "lundi": 0,
        "mardi": 0,
        "mercredi": 0,
        "jeudi": 0,
        "vendredi": 0,
        "samedi": 0,
        "dimanche": 0
    }
    current_date = periode[0]
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

    df_jour_semaine['% Visionnage film']=df_jour_semaine['Nombre']/df_jour_semaine['Nombre écoulé']*100
    df_jour_semaine['% Visionnage au ciné']=df_jour_semaine['Ciné num']/df_jour_semaine['Nombre écoulé']*100


    df_jour_semaine_long = df_jour_semaine.reset_index().melt(
        id_vars='Jour semaine',
        value_vars=['% Visionnage film', '% Visionnage au ciné'],
        var_name='Type',
        value_name='Pourcentage'
    )
    fig_bar_jour_semaine_pourcentage = px.bar(
        df_jour_semaine_long,
        x='Jour semaine',
        y='Pourcentage',
        color='Type',
        color_discrete_map={
            '% Visionnage film': 'blue',
            '% Visionnage au ciné': 'red'
        },
        barmode='group',  # Affiche les barres côte à côte
        category_orders={'Jour semaine': jours_semaine_ordre},
        title='Jours de la semaine où je regarde un film',
    )

    #fig_bar_jour_semaine_pourcentage=px.bar(df_jour_semaine,x=df_jour_semaine.index,y='% Jour semaine',category_orders={'Jour semaine':jours_semaine_ordre})
    a,b=st.columns(2)
    with a:
        st.plotly_chart(fig_line)
    with b:
        st.plotly_chart(fig_bar_jour_semaine_pourcentage)
    c,d=st.columns([1,4])
    with c:
        st.plotly_chart(fig_pie)
    with d:
        st.plotly_chart(fig_treemap_avec)

else:
    st.error("Impossible de charger les données.")

