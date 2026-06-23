from dataclasses import dataclass

@dataclass
class Movie:
    title: str = ""
    director: str = ""
    starring: str = ""
    genres: str = ""
    quality: str = ""
    language: str = ""
    rating: str = ""
    updated: str = ""

    poster: str = ""
    poster_path: str = ""

    page_url: str = ""

@dataclass
class MovieQualities:
    p1080: str | None = None
    p720: str | None = None
    p360: str | None = None