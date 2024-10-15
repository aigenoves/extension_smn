from datetime import date, timedelta
import streamlit as st
from func.stats import per_day
from smn_stats import info_per_year
from func import smn_data

st.set_page_config(
    page_title="Visualizador de datos climáticos", layout="wide", page_icon="📍"
)


stations_data = smn_data.process_stations_data()
station_choices = smn_data.stations(stations_data)
stats_per_day = None

padding = 0


st.markdown(
    """
    <style>
    .small-font {
        font-size:12px;
        font-style: italic;
        color: #b1a7a6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar.form(key="my_form"):
    selectbox_station = st.selectbox(
        "Elija una estación", station_choices, index=None, placeholder="-"
    )
    selectbox_time_period = st.selectbox(
        "Elija un período de tiempo", ["Día", "Mes", "Año"], index=None, placeholder="-"
    )
    selected_date = st.date_input(
        "Seleccione una fecha",
        value=date.today() - timedelta(days=1),
        format="DD/MM/YYYY",
    )

    pressed = st.form_submit_button("Siguiente")

if pressed:
    per_day(selectbox_station, selected_date)


# match sb_menu:
#     case "Temperatura":
#         pick_day()
#     case "Info por ubicación y año":
#         info_per_year()
