from datetime import date
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from func.smn_data import get_station_data
from func import utils
from graphs.windrose import windrose


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
        rosa_vientos = windrose(filtered_data)
        col1, col2 = st.columns(2)

        with col2:
            st.plotly_chart(rosa_vientos)
