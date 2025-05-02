import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime,date, timedelta
from data import load_data

df = load_data()

df_cine=df[df['Ciné'] =='oui']

fig_treemap_lieu = px.treemap(df, path=['Visionnage'], title="Vu avec ...")
st.plotly_chart(fig_treemap_lieu)

fig_treemap_lieu_cine = px.treemap(df_cine, path=['Visionnage'], title="Vu avec ...")
st.plotly_chart(fig_treemap_lieu_cine)