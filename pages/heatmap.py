import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from func.smn_data import proccess_smn_data, process_stations_data

st.set_page_config(
    page_title="Mapa de Calor",
    layout="wide",
)

data_datos = proccess_smn_data()
data_coordenadas = process_stations_data()


data_datos["fecha_hora"] = pd.to_datetime(data_datos["fecha_hora"])
anios = sorted(data_datos["fecha_hora"].dt.year.unique())
st.sidebar.page_link("app.py", label="Volver")
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


mapa = folium.Map(
    location=[-34.61, -58.38],
    zoom_start=5,
    tiles="https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png",
    attr='&copy; <a href="http://www.argenmap.com.ar">Argenmap</a>',
) 

heat_data = [
    [row["lat"], row["lon"], row["dias_calor"]] for _, row in data_combined.iterrows()
]


HeatMap(data=heat_data, radius=15).add_to(mapa)


st.title("Mapa de Calor de Días de Temperatura")
st.write(f"Temperaturas {tipo_texto} {condicion_texto} en el año {anio_seleccionado}")


st_folium(mapa, width=700, height=500)


