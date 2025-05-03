import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data


#st.set_page_config(layout="wide")
df = load_data()

onglet = st.sidebar.radio(
    "Sous-onglets",
    ["Par genre", "Boxplot global"],
    index=0)

min_date = df.index.min()
max_date = df.index.max()

if onglet=='Par genre':
    genre_principal = st.selectbox(
        "Choisissez un Genre Principal",
        options=df['Genre principal'].unique(),
        index=1  # Option par défaut
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
        title="Répartition des notes personnelles",
        labels={'Note': 'Note (sur 10)'},
        range_x=[0, 10.5],       
        color_discrete_sequence=["blue"], 
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
        range_x=[0, 10.5],       
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





    col1, col2 = st.columns(2)  
    with col1:
        a,b=st.columns([3,1])
        with a:
            st.plotly_chart(fig1)
        with b: 
            st.metric("Nombre :",f"{df_filtered['Note'].count()}")
            st.metric("Note moyenne :",f"{df_filtered['Note'].mean():.2f}")
            st.metric("Ecart-type :",f"{df_filtered['Note'].std():.2f}")
            
        
    with col2:
        c,d=st.columns([3,1])
        with c:
            st.plotly_chart(fig2)
        with d: 
            st.metric("Nombre :",f"{df_filtered['Eugénie'].count()}")
            st.metric("Note moyenne :",f"{df_filtered['Eugénie'].mean():.2f}")
            st.metric("Ecart-type :",f"{df_filtered['Eugénie'].std():.2f}")

    st.dataframe(df_filtered[['Nom', 'Année', 'Pays','Note à chaud', 'Note', 'Eugénie','Box office fr (M)']])

    #fig4 = px.line(
        #df_filtered,
        #x=df_filtered.index,                # Axe X : noms des films
        #y=["Note_MA","Note_EWM"],   # Deux séries : notes originales et moyenne mobile
        #labels={"value": "MA", "variable": "EWM"},
        #title="Notes des films et moyenne mobile",)
    #st.plotly_chart(fig4)

else:
    df_long = pd.melt(df, 
                  id_vars=['Genre principal'], 
                  value_vars=['Note', 'Eugénie'], 
                  var_name='Type', 
                  value_name='Valeur')
    
    df_genre = df.groupby('Genre principal')['Note'].agg(Médiane='median').reset_index()
    genre_tries = df_genre.sort_values(by='Médiane', ascending=False)['Genre principal'].tolist()

    fig = px.box(df_long, 
             x='Valeur', 
             y='Genre principal', 
             color='Type', 
             color_discrete_map={'Note': 'blue', 'Eugénie': 'red'},
             height=1000, 
             category_orders={'Genre principal': genre_tries},
             range_x=[0, 10],
             title='Boxplot des notes et Eugénie pour chaque genre')
    
    st.plotly_chart(fig)

    '''df_genre = df.groupby('Genre principal')['Note'].agg(
        Médiane= 'median',
        Moyenne='mean',
        Ecart_type='std',  
        Nombre= 'count').reset_index()
    genre_tries = df_genre.sort_values(by='Médiane',ascending=False)['Genre principal'].tolist()
    fig_box_genres=px.box(data_frame=df, x='Note', y='Genre principal',height=800,category_orders={'Genre principal': genre_tries},range_x=[0, 10],
                          title='Boxplot des notes pour chaque genre')
    
    df_genre_eugenie = df.groupby('Genre principal')['Eugénie'].agg(
        Médiane= 'median',
        Moyenne='mean',
        Ecart_type='std',  
        Nombre= 'count').reset_index()
    fig_box_genres_eugenie=px.box(df, x='Eugénie', y='Genre principal',height=800,category_orders={'Genre principal': genre_tries},range_x=[0, 10],
                          title='Boxplot des notes pour chaque genre')
    
    a,b=st.columns(2)
    with a:
        st.plotly_chart(fig_box_genres)
    with b:
        st.plotly_chart(fig_box_genres_eugenie)
    st.dataframe(df_genre.sort_values('Moyenne',ascending=False)[['Genre principal', 'Moyenne','Ecart_type','Nombre']])'''