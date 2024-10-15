import pandas as pd
import plotly.graph_objects as go


def _get_pressure_color(presion):
    if presion < 1000:
        return "#FF8D33"
    if presion < 1020:
        return "#A8DAB5"
    else:
        return "#007BFF"
    wins_median = df.groupby("punto_cardinal", as_index=False).agg(
        {"viento_v": "median"}
    )


def pressure(filtered_data: pd.Series) -> go.Indicator:
    pressure_median = float(filtered_data["presion"].median())
    graph = go.Indicator(
        mode="gauge+number",
        number={"font": {"size": 25}, "suffix": " hPa"},
        value=pressure_median,
        title={"text": "Presión", "font": {"size": 20}},
        gauge={
            "axis": {"range": [900, 1100]},
            "bar": {
                "color": _get_pressure_color(pressure_median),
                "thickness": 0.3,
            },
        },
    )
    return graph


def temperature(filtered_data: pd.Series) -> go.Indicator:
    temperature_median = float(filtered_data["temperatura"].median())
    graph = go.Indicator(
        mode="gauge+number",
        number={"font": {"size": 25}, "suffix": " °c"},
        value=temperature_median,
        title={"text": "Temperatura", "font": {"size": 20}},
        gauge={
            "axis": {"range": [-50, 50], "tickwidth": 1, "tickcolor": "darkblue"},
            "bar": {"color": "red", "thickness": 0.3},
            "bgcolor": "white",
            "steps": [
                {"range": [-50, 0], "color": "lightblue"},
                {"range": [0, 15], "color": "lightgreen"},
                {"range": [15, 30], "color": "lightyellow"},
                {"range": [30, 50], "color": "indianred"},
            ],
        },
    )
    return graph
