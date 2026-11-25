
import json
from pathlib import Path
import requests

API_URL = "https://ghibliapi.vercel.app/films"
SNAPSHOT = Path(__file__).parent / "data" / "films_snapshot.json"


def clean_films(raw):
    
    if not isinstance(raw, list):
        raise ValueError("Expected a list of films.")
    films = []
    for item in raw:
        try:
            film = {
                "id": item["id"], "Title": item["title"],
                "Director": item["director"], "Year": int(item["release_date"]),
                "Runtime (min)": int(item["running_time"]),
                "RT score (%)": int(item["rt_score"]),
                "Synopsis": item.get("description", "No synopsis available."),
            }
            if not 0 <= film["RT score (%)"] <= 100 or film["Runtime (min)"] <= 0:
                continue
            films.append(film)
        except (KeyError, ValueError, TypeError):
            continue
    if not films:
        raise ValueError("No usable film records were returned.")
    return films


def load_films():
    
    try:
        response = requests.get(API_URL, timeout=15)
        response.raise_for_status()
        return clean_films(response.json()), "live"
    except (requests.RequestException, ValueError):
        raw = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
        return clean_films(raw), "snapshot"


def filter_films(films, directors, years, min_score, max_runtime):
    
    return [f for f in films if
            f["Director"] in directors and years[0] <= f["Year"] <= years[1]
            and f["RT score (%)"] >= min_score and f["Runtime (min)"] <= max_runtime]
