from models import Movie


def print_movies(
    movies: list[Movie],
) -> None:

    for index, movie in enumerate(
        movies,
        start=1,
    ):
        print()

        print(f"[{index}] {movie.title}")
        print(f"Director : {movie.director}")
        print(f"Genres   : {movie.genres}")
        print(f"Rating   : {movie.rating}")
        print(f"Poster   : {movie.poster}")