from datetime import date, timedelta
import streamlit as st
from func import smn_data, utils
from tablero import diario

st.set_page_config(page_title="Datos climáticos del SMN", page_icon=":mostly_sunny:")
stations_data = smn_data.process_stations_data()
station_choices = tuple(smn_data.stations(stations_data))
# heat_map = st.Page("heatmap.py", title="Mapa de Calor")


def main():
    selected_date = None
    selected_month = None
    selected_year = None
    selected_season = None

    with st.sidebar:
        st.sidebar.page_link("app.py", label="Volver")
        stations_options = station_choices
        selected_station = st.selectbox(
            label="Elija la estación meteorológica:",
            options=stations_options,
            index=None,
            placeholder="Selecione una estación met.",
        )
        period_options = ("Día", "Mes", "Año", "Estación del año")
        selected_period = st.selectbox(
            label="Elija tipo de período:",
            options=period_options,
            index=None,
            placeholder="Selecione una opción...",
        )
        if selected_period == "Día":
            selected_date = st.date_input(
                "Seleccione una fecha",
                value=date.today() - timedelta(days=1),
                format="DD/MM/YYYY",
            )
        elif selected_period == "Mes":
            selected_month = st.selectbox(
                label="Elija el mes:",
                options=(utils.MONTHS.keys()),
                index=None,
                placeholder="Selecione un mes...",
            )
            selected_year = st.selectbox(
                label="Elija un año:",
                options=(utils.YEARS_IN_DATA),
                index=None,
                placeholder="Selecione un año...",
            )

        elif selected_period == "Estación del año":
            selected_season = st.selectbox(
                label="Elija una estación del año:",
                options=(utils.YEAR_SEASONS),
                index=None,
                placeholder="Selecione una estación del año...",
            )
            selected_year = st.selectbox(
                label="Elija un año:",
                options=(utils.YEARS_IN_DATA),
                index=None,
                placeholder="Selecione un año...",
            )
        elif selected_period == "Año":
            selected_year = st.selectbox(
                label="Elija un año:",
                options=(utils.YEARS_IN_DATA),
                index=None,
                placeholder="Selecione un año...",
            )

    if selected_date:
        diario.page(selected_station, day=selected_date)
    if selected_month and selected_year:
        diario.page(selected_station, month=selected_month, year=selected_year)
    if selected_season and selected_year:
        diario.page(selected_station, season=selected_season, year=selected_year)
    if selected_year and not selected_month and not selected_season:
        diario.page(selected_station, year=selected_year)


if __name__ == "__main__":

    main()

    # with st.sidebar:
    #     st.markdown("---")
    #     st.markdown(
    #         "<h4>Hecho con:</h4>",
    #         unsafe_allow_html=True,
    #     )
    #     st.markdown(
    #         '<a href="https://pandas.pydata.org/"><img src="https://pandas.pydata.org/static/img/pandas_white.svg" alt="Pandas logo" height="18"></a>',
    #         unsafe_allow_html=True,
    #     )

    #     st.markdown(
    #         '<a href="https://streamlit.io/"><img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16"></a>',
    #         unsafe_allow_html=True,
    #     )
    #     st.markdown(
    #         '<a href="https://plotly.com/"><img src="https://studyopedia.com/wp-content/uploads/2023/07/Plotly-Python-Library.jpg" alt="Plotly logo" height="26"></a>',
    #         unsafe_allow_html=True,
    #     )
    #     st.markdown(
    #         '<a href="https://python.org/"><img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg" alt="Python logo" height="32"></a>',
    #         unsafe_allow_html=True,
    #     )

    #     st.markdown(
    #         '<h6>Proyecto de Extensón &nbsp<img src="https://www.info.unlp.edu.ar/wp-content/uploads/2019/07/logoo-300x300.jpg" alt="UNLP logo" height="22"></h6>',
    #         unsafe_allow_html=True,
    #     )

# &nbsp por <a href="https://github.com/aigenoves">aigenoves</a>
