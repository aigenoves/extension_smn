import streamlit as st


def menu():
    st.sidebar.page_link("pages/stats.py", label="Gráficos por Períodos")
    st.sidebar.page_link("pages/heatmap.py", label="Mapa de Calor")
    st.sidebar.page_link("pages/stations.py", label="Estaciones Meteorológicas")
    st.markdown(
        "<h4>Hecho con:</h4>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<a href="https://pandas.pydata.org/"><img src="https://pandas.pydata.org/static/img/pandas_white.svg" alt="Pandas logo" height="24"></a>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<a href="https://streamlit.io/"><img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="22"></a>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<a href="https://plotly.com/"><img src="https://studyopedia.com/wp-content/uploads/2023/07/Plotly-Python-Library.jpg" alt="Plotly logo" height="26"></a>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<a href="https://python.org/"><img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg" alt="Python logo" height="32"></a>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h6>Proyecto de Extensón &nbsp<img src="https://www.info.unlp.edu.ar/wp-content/uploads/2019/07/logoo-300x300.jpg" alt="UNLP logo" height="22"></h6>',
        unsafe_allow_html=True,
    )
