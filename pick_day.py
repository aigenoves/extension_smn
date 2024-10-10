from datetime import date, timedelta
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from func.smn_data import proccess_smn_data, locations
from func.utils import angulo_a_cardinal


PUNTOS_CARDINALES = [
    {"punto_cardinal": "N", "viento_d": 0},
    {"punto_cardinal": "NE", "viento_d": 45},
    {"punto_cardinal": "E", "viento_d": 90},
    {"punto_cardinal": "SE", "viento_d": 135},
    {"punto_cardinal": "S", "viento_d": 180},
    {"punto_cardinal": "SW", "viento_d": 225},
    {"punto_cardinal": "W", "viento_d": 270},
    {"punto_cardinal": "NW", "viento_d": 315},
]
DF_PUNTOS_CARDINALES = pd.DataFrame(PUNTOS_CARDINALES)


def pick_day():

    df = proccess_smn_data()

    ubicaciones = locations(df)
    ubicacion_seleccionada = st.selectbox(
        "Seleccione una ubicación", ubicaciones, key="ubicaciones"
    )

    fecha_seleccionada = st.date_input(
        "Seleccione una fecha",
        value=date.today() - timedelta(days=1),
        format="DD/MM/YYYY",
    )

    datos_filtrados = filtrar_datos(df, ubicacion_seleccionada, fecha_seleccionada)

    st.write(f"Datos para {ubicacion_seleccionada} en la fecha {fecha_seleccionada}:")
    st.dataframe(datos_filtrados, use_container_width=True)

    graficar_temperatura_presion(datos_filtrados)

    graficar_rosa_vientos(datos_filtrados)


def filtrar_datos(df, ubicacion_seleccionada, fecha_seleccionada):
    datos_filtrados = df[
        (df["ubicacion"] == ubicacion_seleccionada)
        & (df["fecha_hora"].dt.date == fecha_seleccionada)
    ]

    datos_filtrados = datos_filtrados.drop(["ubicacion"], axis=1)
    nuevo_orden = [
        "fecha_hora",
        "temperatura",
        "humedad",
        "presion",
        "viento_d",
        "viento_v",
    ]
    datos_filtrados = datos_filtrados[nuevo_orden]
    datos_filtrados = datos_filtrados.reset_index(drop=True)
    return datos_filtrados.sort_values(by="fecha_hora")


def graficar_temperatura_presion(datos_filtrados):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=datos_filtrados["fecha_hora"].dt.hour,
            y=datos_filtrados["temperatura"],
            mode="lines+markers",
            name="Temperatura",
            line=dict(color="darkred"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=datos_filtrados["fecha_hora"].dt.hour,
            y=datos_filtrados["presion"],
            mode="lines+markers",
            name="Presión (hPa)",
            line=dict(color="darkseagreen"),
            yaxis="y2",
        )
    )

    fig.update_layout(
        title="Temperatura y Presión durante el día",
        xaxis_title="Hora",
        yaxis_title="Temperatura (°C)",
        yaxis=dict(showgrid=True),
        yaxis2=dict(
            title="Presión (hPa)",
            overlaying="y",
            side="right",
            showgrid=False,
            type="log",
        ),
        xaxis=dict(tickformat="%H:%M", showgrid=True),
        template="plotly_white",
    )

    st.plotly_chart(fig)


def graficar_rosa_vientos(datos_filtrados):
    if not datos_filtrados.empty:
        datos_filtrados["punto_cardinal"] = datos_filtrados["viento_d"].apply(
            angulo_a_cardinal
        )

        datos_viento = datos_filtrados.groupby("punto_cardinal", as_index=False).agg(
            {"viento_v": "mean"}
        )

        datos_completos = pd.merge(
            DF_PUNTOS_CARDINALES, datos_viento, on="punto_cardinal", how="left"
        )

        fig_windrose = px.bar_polar(
            datos_completos,
            r="viento_v",
            theta="punto_cardinal",
            color="viento_v",
            color_discrete_sequence=px.colors.sequential.Plasma_r,
            title="Rosa de los Vientos",
            template="plotly_dark",
        )

        st.plotly_chart(fig_windrose)
