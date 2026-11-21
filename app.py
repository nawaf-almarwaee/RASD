from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="رَصْد | RASD", page_icon="💧", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding: 0 !important; max-width: 100% !important;}
[data-testid="stAppViewContainer"] {background: #edf3f2;}
iframe {border: 0;}
</style>
""", unsafe_allow_html=True)

html = (Path(__file__).parent / "dashboard.html").read_text(encoding="utf-8")
components.html(html, height=1300, scrolling=True)
