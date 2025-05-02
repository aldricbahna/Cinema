import streamlit as st
from data import load_data
import plotly.express as px
st.set_page_config(layout="wide")

df = load_data()


if df is not None:
    st.title("Web-app Cinema")
    df['Nb films vus'] = range(1, len(df) + 1)

    fig_line=px.line(df['Nb films vus'],title='Evolution du nombre de films vus en fonction du temps')
    st.plotly_chart(fig_line)

    fig_pie=px.pie(df,'Ciné',title="Vu au cinéma ?")
    st.plotly_chart(fig_pie)

    fig_treemap_avec = px.treemap(df, path=['Avec'], title="Vu avec ...")
    st.plotly_chart(fig_treemap_avec)


    st.write("Aperçu du dataset :")
    st.dataframe(df)

else:
    st.error("Impossible de charger les données.")

