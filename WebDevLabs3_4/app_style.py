
import streamlit as st


def setup(title):
    st.set_page_config(page_title=title + " | ReelScope", page_icon="🎬", layout="wide")
    st.sidebar.title("🎬 ReelScope")
    st.sidebar.caption("Small catalog. Big imagination.")
