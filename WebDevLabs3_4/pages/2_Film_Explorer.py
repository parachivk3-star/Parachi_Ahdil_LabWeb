import pandas as pd
import streamlit as st
from app_style import setup
from film_data import load_films, filter_films

setup("Film Explorer")
st.title("Your movie night, by the numbers.")
st.write("Narrow the catalog, compare the results and pick a film to explore.")

@st.cache_data(ttl=3600, show_spinner=False)
def cached_films():
    return load_films()

if st.sidebar.button("Refresh film data"):
    cached_films.clear()
try:
    with st.spinner("Opening the film catalog…"):
        films, source = cached_films()
except (OSError, ValueError):
    st.error("The catalog is unavailable. Please try again later or restore data/films_snapshot.json.")
    st.stop()
if source == "snapshot":
    st.warning("Live API unavailable. Showing a saved API response retrieved November 23, 2026; these are not live ratings.")


st.sidebar.subheader("Make it your movie night")
directors = st.sidebar.multiselect("Directors", sorted({f["Director"] for f in films}), default=sorted({f["Director"] for f in films}))
ymin, ymax = min(f["Year"] for f in films), max(f["Year"] for f in films)
years = st.sidebar.slider("Release years", ymin, ymax, (ymin, ymax))
score = st.sidebar.slider("Minimum RT score (%)", 0, 100, 0)
max_minutes = max(f["Runtime (min)"] for f in films)
runtime = st.sidebar.slider("Maximum runtime (minutes)", 1, max_minutes, max_minutes)
filtered = filter_films(films, directors, years, score, runtime)
if not filtered:
    st.info("No films match those filters. Select more directors, lower the minimum score, or increase the runtime.")
    st.stop()
frame = pd.DataFrame(filtered)
a, b, c = st.columns(3)
a.metric("Matching films", len(filtered))
b.metric("Average RT score", f"{frame['RT score (%)'].mean():.1f}%")
c.metric("Average runtime", f"{frame['Runtime (min)'].mean():.0f} min")

left, right = st.columns(2)
with left:
    st.subheader("Compare the ratings")
    rating_data = frame.sort_values("RT score (%)", ascending=False).set_index("Title")
    st.bar_chart(rating_data[["RT score (%)"]], color="#db9566", height=340)
with right:
    st.subheader("Time vs. reception")
    st.caption("Each point is a matching film. Hover to see its title.")
    st.scatter_chart(frame.set_index("Title"), x="Runtime (min)", y="RT score (%)", color="#7fc8be", height=340)

st.divider()
st.subheader("Spotlight a film")
selected_title = st.selectbox("Choose a matching film", sorted(frame["Title"].tolist()))
selected = next(f for f in filtered if f["Title"] == selected_title)
with st.container(border=True):
    st.subheader(selected["Title"])
    st.caption(f"{selected['Director']} · {selected['Year']} · {selected['Runtime (min)']} minutes · RT {selected['RT score (%)']}%")
    with st.expander("Read synopsis (may contain spoilers)"):
        st.write(selected["Synopsis"])
    st.write(f"This film is {abs(selected['Runtime (min)'] - frame['Runtime (min)'].mean()):.0f} minutes {'longer' if selected['Runtime (min)'] >= frame['Runtime (min)'].mean() else 'shorter'} than the average of your filtered selection.")

