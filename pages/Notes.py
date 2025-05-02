import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime,date, timedelta
from data import load_data

#st.set_page_config(layout="wide")
df = load_data()


st.dataframe(df)

ajd= datetime.now()
j_moins_30 = ajd - timedelta(days=30)
min_date_filtered = df.index.min()
max_date_filtered = df.index.max()
ecart_jours=(max_date_filtered-min_date_filtered).days+1


## Histogrammes

fig1 = px.histogram(
    df,
    x='Note',               
    nbins=100,               
    title="Répartition des notes de films",
    labels={'Note': 'Note (sur 10)'},
    range_x=[0, 11],       
    color_discrete_sequence=["blue"]
)
fig1.update_layout(
    xaxis_title="Note",
    yaxis_title="Fréquence",
    title_x=0.5,  
    template="plotly_white",
    xaxis=dict(
        tickmode='array',   
        tickvals=list(range(0, 12)),  
        ticktext=list(range(0, 12)),  
        dtick=1  
    ),
    height=600,
    width=900
)

fig2 = px.histogram(
    df,
    x='Eugénie',               
    nbins=100,               
    title="Répartition des notes d'Eugé",
    labels={'Eugénie': "Notes d'Eugé"},
    range_x=[0, 11],       
    color_discrete_sequence=["pink"]
)
fig2.update_layout(
    xaxis_title="Notes d'Eugé",
    yaxis_title="Fréquence",
    title_x=0.5,  
    template="plotly_white",
    xaxis=dict(
        tickmode='array',   
        tickvals=list(range(0, 12)),  
        ticktext=list(range(0, 12)),  
        dtick=1  
    ),
    height=600,
    width=900
)

## Mise en forme

col1, col2 = st.columns(2)  
with col1:
    a,b=st.columns([3,1])
    with a:
        st.plotly_chart(fig1, use_container_width=True)
    with b: 
        st.metric("Nombre :",f"{df['Note'].count()}",delta=df[df.index>=j_moins_30].shape[0])
        st.metric("Note moyenne :",f"{df['Note'].mean():.2f}")
        st.metric("Ecart-type :",f"{df['Note'].std():.2f}")
        
    
with col2:
    c,d=st.columns([3,1])
    with c:
        st.plotly_chart(fig2, use_container_width=True)
    with d:
        st.metric("Nombre :",f"{df['Eugénie'].count()}")
        st.metric("Note moyenne :",f"{df['Eugénie'].mean():.2f}")
        st.metric("Ecart-type :",f"{df['Eugénie'].std():.2f}")


#df_ordre=df.sort_values(by='Note',ascending=False)[['Nom', 'Réalisateur','Sortie','Note','Eugénie','Genre','Durée']]


c1,c2,c3,c4,c5,c6,c7,c8,c9,c10=st.columns(10)

with c1:
    st.image("Images/interstellar.jpg",width=200)
with c2:
    st.image("Images/Kill Bill.webp",width=200)
with c3:
    st.image("Images/Past Lives.webp",width=200)
with c4:
    st.image("Images/La La Land.jpg",width=190)
with c5:
    st.image("Images/Old Boy.jpg",width=200)
with c6:
    st.image("Images/Le samouraï.webp",width=200)
with c7:
    st.image("Images/Un homme et une femme.jpg",width=200)
with c8:
    st.image("Images/Whiplash.webp",width=200)
with c9:
    st.image("Images/Les affranchis.jpg",width=200)
with c10:
    st.image("Images/Le parrain.webp",width=200)
