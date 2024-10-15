import streamlit as st
import pandas as pd
import plotly.express as px
from func.smn_data import proccess_smn_data, process_stations_data


data_datos = proccess_smn_data()
data_coordenadas = process_stations_data()


data_datos["fecha_hora"] = pd.to_datetime(data_datos["fecha_hora"])
anios = sorted(data_datos["fecha_hora"].dt.year.unique())
anio_seleccionado = st.sidebar.selectbox(
    "Selecciona un año:", anios, index=anios.index(max(anios))
)
temp_desde = st.sidebar.slider(
    "Selecciona la temperatura (°C):", min_value=-15, max_value=50, value=35
)
condicion_temp = st.sidebar.radio(
    "Mostrar días con temperaturas:", ("mayores", "menores")
)
tipo_temp = st.sidebar.selectbox("Filtrar por temperaturas:", ("máximas", "mínimas"))

data_filtrada = data_datos[data_datos["fecha_hora"].dt.year == anio_seleccionado]

data_filtrada["fecha"] = data_filtrada["fecha_hora"].dt.date

if tipo_temp == "máximas":
    data_diaria = (
        data_filtrada.groupby(["ubicacion", "fecha"])["temperatura"].max().reset_index()
    )
    tipo_texto = "máximas"
else:
    data_diaria = (
        data_filtrada.groupby(["ubicacion", "fecha"])["temperatura"].min().reset_index()
    )
    tipo_texto = "mínimas"

if condicion_temp == "mayores":
    data_filtrada_temp = data_diaria[data_diaria["temperatura"] > temp_desde]
    condicion_texto = f"mayores a {temp_desde} °C"
else:
    data_filtrada_temp = data_diaria[data_diaria["temperatura"] < temp_desde]
    condicion_texto = f"menores a {temp_desde} °C"


data_dias_calor = (
    data_filtrada_temp.groupby("ubicacion").size().reset_index(name="dias_calor")
)


data_combined = pd.merge(
    data_dias_calor,
    data_coordenadas,
    left_on="ubicacion",
    right_on="nombre",
    how="inner",
)


fig = px.density_mapbox(
    data_combined,
    lat="lat",
    lon="lon",
    z="dias_calor",
    radius=50,
    center=dict(lat=data_combined["lat"].mean(), lon=data_combined["lon"].mean()),
    zoom=2,
    color_continuous_scale="inferno",
    mapbox_style="carto-positron",
    title=f"Mapa de Calor - Días con temperatura {condicion_texto} {tipo_texto} en {anio_seleccionado}",
)

fig.update_layout(
    coloraxis_colorbar=dict(title=f"Días con Tmax {condicion_texto} {tipo_texto}"),
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
)


st.plotly_chart(fig)
