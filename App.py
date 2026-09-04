import streamlit as st

home = st.Page(
    "Home.py",
    title="Home",
    icon="🏠",
    default=True
)

analysis = st.Page(
    "pages/Analysis.py",
    title="Analysis",
    icon="📊"
)

prediction = st.Page(
    "pages/Prediction.py",
    title="Prediction",
    icon="📝"
)

pg = st.navigation(
    [home, analysis, prediction],
    position="sidebar",
)

pg.run()
