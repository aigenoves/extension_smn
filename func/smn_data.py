from pathlib import Path
import streamlit as st
import pandas as pd


@st.cache_data
def proccess_smn_data():
    main_path = Path(__file__).resolve()
    main_directory = main_path.parent.parent
    relative_path = main_directory / "smn_data"
    df = pd.read_parquet(relative_path / "datosdiarios_smn.parquet", engine="pyarrow")
    return df


@st.cache_data
def stations():
    main_path = Path(__file__).resolve()
    main_directory = main_path.parent.parent
    relative_path = main_directory / "smn_data"
    df = pd.read_parquet(relative_path / "estaciones_smn.parquet", engine="pyarrow")
    return df


@st.cache_data
def locations(df):
    return df["ubicacion"].unique()


@st.cache_data
def years_with_data(df, location):
    df_filtrado = df[df["ubicacion"] == location]

    return df_filtrado["fecha_hora"].dt.year.unique()
