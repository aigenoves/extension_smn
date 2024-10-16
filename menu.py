import streamlit as st


def menu():
    st.sidebar.page_link("pages/stats.py", label="Gráficos por Períodos")
    st.sidebar.page_link("pages/heatmap.py", label="Mapa de Calor")
    st.sidebar.page_link("pages/stations.py", label="Estaciones Meteorológicas")
