from datetime import date, timedelta
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from func.smn_data import proccess_smn_data, locations

# Definir los puntos cardinales con las direcciones correspondientes
puntos_cardinales = [
    {"punto_cardinal": "N", "viento_d": 0},
    {"punto_cardinal": "NE", "viento_d": 45},
    {"punto_cardinal": "E", "viento_d": 90},
    {"punto_cardinal": "SE", "viento_d": 135},
    {"punto_cardinal": "S", "viento_d": 180},
    {"punto_cardinal": "SW", "viento_d": 225},
    {"punto_cardinal": "W", "viento_d": 270},
    {"punto_cardinal": "NW", "viento_d": 315},
]
df_puntos_cardinales = pd.DataFrame(puntos_cardinales)


# Función para mapear ángulos a puntos cardinales
def angulo_a_cardinal(angulo):
    if 337.5 <= angulo or angulo < 22.5:
        return "N"
    elif 22.5 <= angulo < 67.5:
        return "NE"
    elif 67.5 <= angulo < 112.5:
        return "E"
    elif 112.5 <= angulo < 157.5:
        return "SE"
    elif 157.5 <= angulo < 202.5:
        return "S"
    elif 202.5 <= angulo < 247.5:
        return "SW"
    elif 247.5 <= angulo < 292.5:
        return "W"
    elif 292.5 <= angulo < 337.5:
        return "NW"


# Función para seleccionar la ubicación y la fecha, y filtrar los datos correspondientes
def pick_day():
    # Cargar y procesar los datos
    df = proccess_smn_data()

    # Obtener ubicaciones y generar la interfaz para seleccionarlas
    ubicaciones = locations(df)
    ubicacion_seleccionada = st.selectbox("Seleccione una ubicación", ubicaciones)

    # Selección de fecha
    fecha_seleccionada = st.date_input(
        "Seleccione una fecha",
        value=date.today() - timedelta(days=1),
        format="DD/MM/YYYY",
    )

    # Filtrar los datos por ubicación y fecha
    datos_filtrados = filtrar_datos(df, ubicacion_seleccionada, fecha_seleccionada)

    # Mostrar los datos filtrados
    st.write(f"Datos para {ubicacion_seleccionada} en la fecha {fecha_seleccionada}:")
    st.dataframe(datos_filtrados, use_container_width=True)

    # Graficar temperatura y presión
    graficar_temperatura_presion(datos_filtrados)

    # Graficar rosa de los vientos
    graficar_rosa_vientos(datos_filtrados)


# Función para filtrar los datos por ubicación y fecha seleccionada
def filtrar_datos(df, ubicacion_seleccionada, fecha_seleccionada):
    datos_filtrados = df[
        (df["ubicacion"] == ubicacion_seleccionada)
        & (df["fecha_hora"].dt.date == fecha_seleccionada)
    ]

    # Ordenar columnas y preparar el DataFrame filtrado
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


# Función para graficar temperatura y presión a lo largo del día
def graficar_temperatura_presion(datos_filtrados):
    fig = go.Figure()

    # Gráfico de temperatura
    fig.add_trace(
        go.Scatter(
            x=datos_filtrados["fecha_hora"].dt.hour,
            y=datos_filtrados["temperatura"],
            mode="lines+markers",
            name="Temperatura",
            line=dict(color="darkred"),
        )
    )

    # Gráfico de presión en un segundo eje Y
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

    # Configurar el layout del gráfico
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

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)


# Función para graficar la rosa de los vientos
def graficar_rosa_vientos(datos_filtrados):
    if not datos_filtrados.empty:
        # Agregar puntos cardinales según el ángulo
        datos_filtrados["punto_cardinal"] = datos_filtrados["viento_d"].apply(
            angulo_a_cardinal
        )

        # Agrupar los datos por punto cardinal y calcular la velocidad media del viento
        datos_viento = datos_filtrados.groupby("punto_cardinal", as_index=False).agg(
            {"viento_v": "mean"}
        )

        # Completar los datos con todos los puntos cardinales
        datos_completos = pd.merge(
            df_puntos_cardinales, datos_viento, on="punto_cardinal", how="left"
        )

        # Graficar la rosa de los vientos
        fig_windrose = px.bar_polar(
            datos_completos,
            r="viento_v",  # Velocidad del viento
            theta="punto_cardinal",  # Puntos cardinales
            color="viento_v",  # Colorear según la velocidad
            color_discrete_sequence=px.colors.sequential.Plasma_r,
            title="Rosa de los Vientos",
            template="plotly_dark",
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_windrose)


# Llamada inicial para ejecutar el flujo completo
pick_day()
