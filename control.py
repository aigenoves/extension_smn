import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from func.smn_data import proccess_smn_data, locations
from func.wind_rose import windrose


# Función para determinar el color de la barra de humedad
def get_humedad_color(humedad):
    if humedad < 40:
        return "#F5F5DC"
    elif humedad < 70:
        return "#99FF99"
    else:
        return "#003366"


def get_presion_color(presion):
    if presion < 1000:
        return "#FF8D33"
    if presion < 1020:
        return "#A8DAB5"
    else:
        return "#007BFF"


# Función para filtrar datos por ubicación, fecha y hora
def filtrar_datos(df, ubicacion, fecha, hora):
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"])
    df["hora"] = df["fecha_hora"].dt.hour  # Extraemos la hora
    df_filtrado = df[
        (df["ubicacion"] == ubicacion)
        & (df["fecha_hora"].dt.date == fecha)
        & (df["hora"] == hora)
    ]
    return df_filtrado


st.title("Tablero de Control Meteorológico")
st.sidebar.header("Filtros")


df = proccess_smn_data()


ubicaciones = df["ubicacion"].unique()
ubicacion_seleccionada = st.sidebar.selectbox("Selecciona la ubicación", ubicaciones)

fecha_inicio = st.sidebar.date_input("Fecha de inicio", df["fecha_hora"].min().date())


hora = st.sidebar.slider("Hora de inicio", 0, 23, 0)


datos_filtrados = filtrar_datos(df, ubicacion_seleccionada, fecha_inicio, hora)


if datos_filtrados.empty:
    st.warning("No se encontraron datos para los filtros seleccionados.")
else:

    if float(datos_filtrados["presion"]) < 1000:
        clima_icono = "icons/tormenta.png"  # Cambia esta URL
    elif 1000 <= float(datos_filtrados["presion"]) <= 1020:
        clima_icono = "icons/nublado.png"  # Cambia esta URL
    else:
        clima_icono = "icons/sol.png"  # Cambia esta URL

    st.image(clima_icono, width=30)

    # Gráfico tipo Gauge para la presión
    fig_presion = go.Figure(
        go.Indicator(
            mode="gauge+number",
            number={"font": {"size": 25}, "suffix": " hPa"},
            value=float(datos_filtrados["presion"]),
            title={"text": "Presión", "font": {"size": 20}},
            gauge={
                "axis": {"range": [900, 1100]},
                "bar": {
                    "color": get_presion_color(float(datos_filtrados["presion"])),
                    "thickness": 0.3,
                },
            },
            # domain={"row": 1, "column": 0},
        )
    )

    fig_humedad = go.Figure(
        go.Indicator(
            mode="gauge+number",
            number={"font": {"size": 25}, "suffix": " %"},
            value=float(datos_filtrados["humedad"]),
            title={"text": "Humedad", "font": {"size": 20}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {
                    "color": get_humedad_color(float(datos_filtrados["humedad"])),
                    "thickness": 0.3,
                },
            },  # Rango típico de humedad relativa
            # domain={"row": 1, "column": 1},
        )
    )

    fig_temperatura = go.Figure(
        go.Indicator(
            mode="gauge+number",
            number={"font": {"size": 25}, "suffix": " °c"},
            value=float(datos_filtrados["temperatura"]),
            title={"text": "Temperatura", "font": {"size": 20}},
            gauge={
                "axis": {"range": [-10, 50], "tickwidth": 1, "tickcolor": "darkblue"},
                "bar": {"color": "red", "thickness": 0.3},
                "bgcolor": "white",
                "steps": [
                    {"range": [-10, 0], "color": "lightblue"},
                    {"range": [0, 15], "color": "lightgreen"},
                    {"range": [15, 30], "color": "lightyellow"},
                    {"range": [30, 50], "color": "indianred"},
                ],
            },
            # domain={"row": 0, "column": 0},
        )
    )

    rosa_vientos = windrose(
        float(datos_filtrados["viento_d"]), float(datos_filtrados["viento_v"]), 0, 1
    )
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_temperatura)
        st.plotly_chart(fig_presion)
    with col2:
        st.plotly_chart(rosa_vientos)
        st.plotly_chart(fig_humedad)

    # Actualización del layout
    # fig.update_layout(
    #     grid=dict(rows=2, columns=2, pattern="independent"),
    #     margin=dict(l=50, r=50, t=50, b=50),  # Aumentar márgenes
    # )

    # # Mostrar el gráfico en Streamlit
    # st.plotly_chart(fig)
