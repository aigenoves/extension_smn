import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from func.smn_data import proccess_smn_data, locations, years_with_data


def load_data():
    df = proccess_smn_data()
    return df


def get_unique_locations(df):
    return locations(df)


def select_location(all_locations):
    return st.selectbox(
        "Seleccione una ubicación", all_locations, key="ubicacion_seleccionada"
    )


def get_available_years(df, selected_location):
    return years_with_data(df, selected_location)


def select_year(unique_years):
    return st.selectbox(
        "Seleccione un año", sorted(unique_years), key="año_seleccionado"
    )


def filter_data(df, selected_location, selected_year):
    filtered_data = df[
        (df["ubicacion"] == selected_location)
        & (df["fecha_hora"].dt.year == selected_year)
    ]
    return filtered_data


def aggregate_monthly_data(filtered_data: pd.DataFrame):
    filtered_data = filtered_data.copy()
    filtered_data["mes"] = filtered_data["fecha_hora"].dt.month
    agg_data = (
        filtered_data.groupby("mes")
        .agg(
            temperatura_max=("temperatura", "max"),
            temperatura_min=("temperatura", "min"),
        )
        .reset_index()
    )
    return agg_data


def create_candlestick_chart(agg_data, selected_location, selected_year):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=agg_data["mes"],
                open=agg_data["temperatura_min"],
                high=agg_data["temperatura_max"],
                low=agg_data["temperatura_min"],
                close=agg_data["temperatura_max"],
                name="Temperatura",
            )
        ]
    )

    fig.update_layout(
        title=f"Temperatura máxima y mínima en {selected_location} - {selected_year}",
        xaxis_title="Mes",
        yaxis_title="Temperatura (°C)",
        xaxis=dict(
            tickvals=agg_data["mes"],
            ticktext=[
                "Ene",
                "Feb",
                "Mar",
                "Abr",
                "May",
                "Jun",
                "Jul",
                "Ago",
                "Sep",
                "Oct",
                "Nov",
                "Dic",
            ],
        ),
        yaxis_range=[
            agg_data["temperatura_min"].min() - 5,
            agg_data["temperatura_max"].max() + 5,
        ],
    )
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


def create_line_chart(agg_data, selected_location, selected_year):
    line_graph = go.Figure()
    line_graph.add_trace(
        go.Scatter(
            x=agg_data["mes"],
            y=agg_data["temperatura_max"],
            mode="lines+markers",
            name="Temperatura Máxima",
            line=dict(color="red"),
        )
    )
    line_graph.add_trace(
        go.Scatter(
            x=agg_data["mes"],
            y=agg_data["temperatura_min"],
            mode="lines+markers",
            name="Temperatura Mínima",
            line=dict(color="blue"),
        )
    )

    line_graph.update_layout(
        title=f"Temperaturas Máxima y Mínima en {selected_location} - {selected_year}",
        xaxis_title="Mes",
        yaxis_title="Temperatura (°C)",
        xaxis=dict(
            tickvals=agg_data["mes"],
            ticktext=[
                "Ene",
                "Feb",
                "Mar",
                "Abr",
                "May",
                "Jun",
                "Jul",
                "Ago",
                "Sep",
                "Oct",
                "Nov",
                "Dic",
            ],
        ),
    )
    return line_graph


def info_per_year():
    df = load_data()
    all_locations = get_unique_locations(df)
    selected_location = select_location(all_locations)
    unique_years = get_available_years(df, selected_location)
    selected_year = select_year(unique_years)
    filtered_data = filter_data(df, selected_location, selected_year)
    agg_data = aggregate_monthly_data(filtered_data)

    # candlestick_fig = create_candlestick_chart(
    #     agg_data, selected_location, selected_year
    # )
    # st.plotly_chart(candlestick_fig)

    line_graph = create_line_chart(agg_data, selected_location, selected_year)
    st.plotly_chart(line_graph)
