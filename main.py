import asyncio

from scraper import fetch_latest_movies ,start_scraper
from cache import save_movies, download_poster
from tui import Padam

async def main():
    
    movies = await fetch_latest_movies("https://moviesda32.com/home.html")
    print(f"\nFetched {len(movies)} movies")
    for movie in movies:
        filename = (movie.page_url.rstrip("/").split("/")[-1] + ".jpg")
        movie.poster_path = download_poster(movie.poster, filename)
    
    save_movies(movies)
    app = Padam(movies)
    await app.run_async()
    await start_scraper(app.selected_movie.page_url)


if __name__ == "__main__":
    asyncio.run(main())