from textual.app import App, ComposeResult
from textual.widgets import DataTable, Static
from textual.containers import Horizontal
from src.models import Movie


class Padam(App):
    CSS = """
    #movies {
        width: 35%;
        min-width: 40;
    }

    #info {
        width: 1fr;
        border: solid $primary;
        padding: 1 2;
        margin: 1;
    }
    """

    def __init__(self, movies: list[Movie]):
        super().__init__()
        self.movies = movies
        self.selected_movie = None

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield DataTable(id="movies")
            yield Static("Select a movie", id="info")

    def on_mount(self) -> None:
        table = self.query_one("#movies", DataTable)

        table.add_columns("#", "Movie")

        for index, movie in enumerate(self.movies, start=1):
            table.add_row(str(index), movie.title)

        table.cursor_type = "row"

        if self.movies:
            self.update_movie_info(self.movies[0])

    def update_movie_info(self, movie: Movie) -> None:
        info = self.query_one("#info", Static)

        info.update(
            f"""Movie: {movie.title}

Director: {movie.director}
Starring: {movie.starring}
Genres: {movie.genres}
Quality: {movie.quality}
Language: {movie.language}
Movie Rating: {movie.rating}
Last Updated: {movie.updated}
"""
        )

    def on_data_table_row_highlighted(self, event) -> None:
        row = event.cursor_row

        if not (0 <= row < len(self.movies)):
            return

        self.update_movie_info(self.movies[row])

    def on_data_table_row_selected(self, event) -> None:
        self.selected_movie = self.movies[event.cursor_row]
        self.exit()