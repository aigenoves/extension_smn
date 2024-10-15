from datetime import date
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from func.smn_data import get_station_data
from func import utils
from graphs.windrose import windrose
from graphs import gauge


def page(
    estation: str,
    day: date = None,
    month: str = None,
    year: int = None,
    season: str = None,
) -> None:
    filtered_data = get_station_data(
        estation, day=day, month=month, year=year, season=season
    )
    if filtered_data.empty:
        st.warning("No se encontraron datos para los filtros seleccionados.")

    else:
        windrose_graph = windrose(filtered_data)
        pressure_graph = go.Figure(gauge.pressure(filtered_data=filtered_data))
        temperature_graph = go.Figure(gauge.temperature(filtered_data=filtered_data))

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(temperature_graph)

        with col2:
            st.plotly_chart(windrose_graph)
            st.plotly_chart(pressure_graph)
