import pandas as pd
import plotly.express as px
from func.utils import angulo_a_cardinal

PUNTOS_CARDINALES = [
    {"punto_cardinal": "N", "viento_d": 0},
    {"punto_cardinal": "NE", "viento_d": 45},
    {"punto_cardinal": "E", "viento_d": 90},
    {"punto_cardinal": "SE", "viento_d": 135},
    {"punto_cardinal": "S", "viento_d": 180},
    {"punto_cardinal": "SO", "viento_d": 225},
    {"punto_cardinal": "O", "viento_d": 270},
    {"punto_cardinal": "NO", "viento_d": 315},
]
DF_PUNTOS_CARDINALES = pd.DataFrame(PUNTOS_CARDINALES)


def windrose(
    direccion_viento: float, velocidad_viento: float, row: int = 0, col: int = 0
):
    data = DF_PUNTOS_CARDINALES.copy()
    punto_cardinal = angulo_a_cardinal(direccion_viento)

    data["velocidad"] = data["punto_cardinal"].apply(
        lambda x: velocidad_viento if x == punto_cardinal else 0
    )
    fig_windrose = px.bar_polar(
        data,
        r="velocidad",
        theta="punto_cardinal",
        color="velocidad",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        title="Rosa de los Vientos",
        template="plotly_dark",
    )
    fig_windrose.update_traces(width=0.2)
    return fig_windrose
