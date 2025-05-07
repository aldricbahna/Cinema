import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data

df = load_data()

df.rename(columns={'Note':'Aldric'},inplace=True)

df_genre = df.groupby('Genre principal')[['Aldric','Eugénie']].agg(Moyenne_Aldric=('Aldric','mean'),
                                                                   Nombre=('Aldric','count'),
                                                                   Moyenne_Euge=('Eugénie','mean')).reset_index()

df_genre_superieur_2=df_genre[df_genre['Nombre']>2]
df_genre_superieur_2.rename(columns={'Moyenne_Aldric':'Aldric',
                                     'Moyenne_Euge':'Eugénie'}, inplace=True)
#radar=px.line_polar(df_genre,r=['Note','Eugénie'],theta='Genre principal',line_close=True)
#st.plotly_chart(radar)

df_long = pd.melt(
    df_genre_superieur_2,
    id_vars=['Genre principal'],
    value_vars=['Aldric', 'Eugénie'],
    var_name='Prénom',
    value_name='Note'
)

df_long_closed = pd.concat([
    df_long,
    df_long.groupby('Prénom').first().reset_index()
], ignore_index=True)


radar = px.line_polar(
    df_long_closed,
    r='Note',
    theta='Genre principal',
    color='Prénom',
    color_discrete_map={'Aldric': 'blue', 'Eugénie': '#FF007F'},
    height=800,
    width=1500,

)
radar.update_layout(

    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 10]  # Plage des valeurs
        )
    ),
    showlegend=True,
    
)
#radar.update_traces(line=dict(width=3, shape='spline'))
radar.update_traces(fill='toself')
radar.update_traces(mode='lines+markers')
st.plotly_chart(radar)