import streamlit as st
from pick_day import pick_day
from smn_stats import info_per_year

st.header("Ciencia de Datos")
st.subheader("SMN Open Data")

st.sidebar.title("Analisis")

sb_menu = st.sidebar.radio("Tipo", ["Info por ubicación y año", "Temperatura"])
match sb_menu:
    case "Temperatura":
        pick_day()
    case "Info por ubicación y año":
        info_per_year()
