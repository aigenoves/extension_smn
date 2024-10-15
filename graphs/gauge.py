import pandas as pd
import plotly.graph_objects as go


def _get_pressure_color(pressure: float) -> str:
    if pressure < 1000:
        return "#FF8D33"
    if pressure < 1020:
        return "#A8DAB5"
    else:
        return "#007BFF"


def _get_humidity_color(humidity: float) -> str:
    if humidity < 40:
        return "#F5F5DC"
    elif humidity < 70:
        return "#99FF99"
    else:
        return "#003366"


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


def humidity(filtered_data: pd.Series) -> go.Indicator:
    humidity_median = float(filtered_data["humedad"].median())
    graph = go.Indicator(
        mode="gauge+number",
        number={"font": {"size": 25}, "suffix": " %"},
        value=humidity_median,
        title={"text": "Humedad", "font": {"size": 20}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {
                "color": _get_humidity_color(humidity_median),
                "thickness": 0.3,
            },
        },
    )
    return graph
