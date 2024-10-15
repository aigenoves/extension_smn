import pandas as pd
import plotly.express as px
from func import utils


def windrose(df: pd.DataFrame):
    df["punto_cardinal"] = df["viento_d"].apply(utils.angulo_a_cardinal)

    wins_median = df.groupby("punto_cardinal", as_index=False).agg(
        {"viento_v": "median"}
    )

    data_directions = pd.merge(
        utils.DF_PUNTOS_CARDINALES, wins_median, on="punto_cardinal", how="left"
    )

    fig_windrose = px.bar_polar(
        data_directions,
        r="viento_v",
        theta="punto_cardinal",
        color="viento_v",
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        title="Rosa de los Vientos",
        template="plotly_dark",
        labels={'viento_v': 'km/h', 'punto_cardinal': "Dirección"}
    )
    return fig_windrose
