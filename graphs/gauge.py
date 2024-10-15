import pandas as pd
import plotly.graph_objects as go


def _get_presion_color(presion):
    if presion < 1000:
        return "#FF8D33"
    if presion < 1020:
        return "#A8DAB5"
    else:
        return "#007BFF"


def presion(filtered_data: pd.DataFrame) -> go.Indicator:
    go.Indicator(
        mode="gauge+number",
        number={"font": {"size": 25}, "suffix": " hPa"},
        value=float(filtered_data["presion"]),
        title={"text": "Presión", "font": {"size": 20}},
        gauge={
            "axis": {"range": [900, 1100]},
            "bar": {
                "color": _get_presion_color(float(filtered_data["presion"])),
                "thickness": 0.3,
            },
        },
    )
