from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
from func import utils


@st.cache_data
def proccess_smn_data():
    main_path = Path(__file__).resolve()
    main_directory = main_path.parent.parent
    relative_path = main_directory / "smn_data"
    df = pd.read_parquet(relative_path / "datosdiarios_smn.parquet", engine="pyarrow")
    df["punto_cardinal"] = df["viento_d"].apply(utils.angulo_a_cardinal)
    return df


@st.cache_data
def process_stations_data():
    main_path = Path(__file__).resolve()
    main_directory = main_path.parent.parent
    relative_path = main_directory / "smn_data"
    df = pd.read_parquet(relative_path / "estaciones_smn.parquet", engine="pyarrow")
    return df


@st.cache_data
def stations(df: pd.DataFrame):
    return df["nombre"].unique()


@st.cache_data
def locations(df):
    return df["ubicacion"].unique()


@st.cache_data
def years_with_data(df, location):
    df_filtrado = df[df["ubicacion"] == location]

    return df_filtrado["fecha_hora"].dt.year.unique()


# Función para filtrar datos por ubicación, fecha y hora
def get_station_data(
    ubicacion: str,
    day: datetime.date = None,
    month: str = None,
    year: int = None,
    season: str = None,
) -> pd.DataFrame:
    if day is not None and (
        month is not None or year is not None or season is not None
    ):
        raise ValueError(
            "Si se proporciona 'day', no pueden ser proporcionados 'month', 'year' ni 'season'."
        )

    if month is not None and (year is None or season is not None):
        raise ValueError(
            "Si se proporciona 'month', debe acompañarse con 'year' y no puede haber 'season' ni 'day'."
        )

    if year is not None and (
        day is not None or (season is not None and month is not None)
    ):
        raise ValueError(
            "Si se proporciona 'year', puede acompañarse con 'month' o 'season', pero no ambos ni 'day'."
        )

    if season is not None and (day is not None or month is not None):
        raise ValueError(
            "Si se proporciona 'season', puede acompañarse con 'year', pero no con 'day' ni 'month'."
        )

    df = proccess_smn_data()
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"])
    df["hora"] = df["fecha_hora"].dt.hour  # Extraemos la hora

    if day:
        df_filtrado = df[
            (df["ubicacion"] == ubicacion) & (df["fecha_hora"].dt.date == day)
        ]
    if season:
        df_filtrado = df[
            (df["ubicacion"] == ubicacion) & (df["fecha_hora"].dt.year == year)
        ]
        df_filtrado = df_filtrado[
            (df_filtrado["ubicacion"] == ubicacion)
            & (df_filtrado["fecha_hora"].apply(lambda day: utils.season(day, season)))
        ]

    if month:
        df_filtrado = df[
            (df["ubicacion"] == ubicacion)
            & (df["fecha_hora"].dt.year == year)
            & (df["fecha_hora"].dt.month == utils.MONTHS[month])
        ]

    if year and not month and not season:
        df_filtrado = df[
            (df["ubicacion"] == ubicacion) & (df["fecha_hora"].dt.year == year)
        ]
    return df_filtrado
