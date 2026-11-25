
import streamlit as st
from app_style import setup

setup("ReelScope")

st.title("Find your next movie night.")
st.write("Explore the storytelling of Studio Ghibli through film data, then talk movies with an AI companion.")
a, b = st.columns(2)
with a:
    with st.container(border=True):
        st.subheader("01 · Explore the films")
        st.write("Filter by director, release year, rating, and runtime. Compare films with two interactive charts and discover a title that fits your evening.")
        st.page_link("pages/2_Film_Explorer.py", label="Open Film Explorer", icon="🎬")
with b:
    with st.container(border=True):
        st.subheader("02 · Talk cinema")
        st.write("Discuss animation, storytelling, and movie preferences. The chatbot remembers this session, but cannot look up live film data.")
        st.page_link("pages/3_Movie_Chatbot.py", label="Open Movie Chatbot", icon="💬")
st.divider()
st.subheader("Why this project?")
st.write("ReelScope connects computing with entertainment analytics: converting API data into numbers, filtering a catalog, and visualizing patterns that help audiences explore films. These skills also apply to data science and recommendation products.")

st.subheader("Our team")
st.write("CS 1301 · Fall 2026")
st.write("Parachi Kumari and Ahdil Singh · Team 78 · Section D")
