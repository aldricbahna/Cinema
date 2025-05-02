import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data

df = load_data()

df.rename(columns={'Note':'Aldric'},inplace=True)
df_genre=df.groupby('Genre principal')[['Aldric','Eugénie']].mean().reset_index()

st.dataframe(df_genre)

#radar=px.line_polar(df_genre,r=['Note','Eugénie'],theta='Genre principal',line_close=True)
#st.plotly_chart(radar)

df_long = pd.melt(
    df_genre,
    id_vars=['Genre principal'],
    value_vars=['Aldric', 'Eugénie'],
    var_name='Prénom',
    value_name='Note'
)

st.dataframe(df_long)

radar = px.line_polar(
    df_long,
    r='Note',
    theta='Genre principal',
    color='Prénom',
    color_discrete_map={'Aldric': 'blue', 'Eugénie': '#FF007F'},
    height=800,
    width=1500
)
radar.update_layout(

    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 10]  # Plage des valeurs
        )
    ),
    showlegend=True,
    legend=dict(
        x=1.1,  # Position à droite
        y=1.1
    )
)

st.plotly_chart(radar)