
import httpx
import json
from pathlib import Path
from dataclasses import asdict

CACHE_DIR = Path("cache")
POSTERS_DIR = CACHE_DIR / "posters"

CACHE_DIR.mkdir(exist_ok=True)
POSTERS_DIR.mkdir(exist_ok=True)

MOVIES_CACHE = CACHE_DIR / "movies.json"

def save_movies(movies):
    with open(MOVIES_CACHE, "w") as file:
        json.dump(
            [asdict(movie) for movie in movies],
            file,
            indent=2,
        )


def load_movies():
    if not MOVIES_CACHE.exists():
        return []

    with open(MOVIES_CACHE) as file:
        return json.load(file)
    

def download_poster(url: str, filename: str) -> str:
    path = POSTERS_DIR / filename

    if path.exists():
        return str(path)

    response = httpx.get(url)
    response.raise_for_status()

    path.write_bytes(response.content)

    return str(path)