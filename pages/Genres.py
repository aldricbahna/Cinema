import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data


#st.set_page_config(layout="wide")
df = load_data()


st.dataframe(df)

st.title("Notes de films")

min_date = df.index.min()
max_date = df.index.max()

'''
data_range = st.slider(
    label="Sélectionnez la plage de dates",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)'''

genre_principal = st.selectbox(
    "Choisissez un Genre Principal",
    options=df['Genre principal'].unique(),
    index=0  # Option par défaut
)


#df_filtered = df[(df.index >= data_range[0]) & (df.index <= data_range[1]) & (df['Genre principal'] == genre_principal)]
df_filtered = df[df['Genre principal'] == genre_principal]
min_date_filtered = df_filtered.index.min()
max_date_filtered = df_filtered.index.max()
ecart_jours=(max_date_filtered-min_date_filtered).days+1

fig1 = px.histogram(
    df_filtered,
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
    df_filtered,
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

df_filtered["Note_MA"] = df_filtered["Note"].rolling(window=f"{ecart_jours}D").mean()
df_filtered["Note_EWM"] = df_filtered["Note"].ewm(alpha=0.5).mean()
tend=(df_filtered["Note_MA"].iloc[-1]-df_filtered["Note_MA"].iloc[-2]).round(2)
st.write(tend)


col1, col2 = st.columns(2)  
with col1:
    a,b=st.columns([3,1])
    with a:
        st.plotly_chart(fig1, use_container_width=True)
    with b: 
        st.metric("Nombre :",f"{df_filtered['Note'].count()}")
        st.metric("Note moyenne :",f"{df_filtered['Note'].mean():.2f}",delta=tend)
        st.metric("Ecart-type :",f"{df_filtered['Note'].std():.2f}")
        
    
with col2:
    st.plotly_chart(fig2, use_container_width=True)


fig4 = px.line(
    df_filtered,
    x=df_filtered.index,                # Axe X : noms des films
    y=["Note_MA","Note_EWM"],   # Deux séries : notes originales et moyenne mobile
    labels={"value": "MA", "variable": "EWM"},
    title="Notes des films et moyenne mobile",
)
st.plotly_chart(fig4)

st.dataframe(df_filtered["Note_MA"])