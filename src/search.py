from src.constant import DOMAIN , HEADERS, HOME
from urllib.parse import urljoin
from src.scraper import Scraper
from InquirerPy import inquirer
from InquirerPy.base import Choice
import httpx


class Search:
    def __init__(self):
        self.search_url = None
        self.results = []
        self.selected_movie = None
        self.selected_quality_href = None
        self.selected_server_url = None

        self.scraper = Scraper()

    #parse the base url for search
    def parse_search_url(self, query:str, year: str | None=None) -> None:
        if year:
            self.search_url = urljoin(DOMAIN,f"/tamil-{year}-movies/")
        else:
            href = query[0].lower()
            self.search_url = urljoin(DOMAIN ,f"/tamil-movies/{href}/")

    #search in the parsed base url
    async def search_movie_url(self, query:str, year:str | None=None) -> list[dict[str, str]]:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            pages = await self.scraper.get_pagination_pages(client, self.search_url)
            for page in pages:
                links = await self.scraper.extract_links(client,page)
                for text, href in links:
                    movie = {"title": text, "movie_url": urljoin(DOMAIN,href)}
                    if query.lower() in text.lower():
                        self.results.append(movie)

            return self.results
        
    #used only for fetch latest added movies
    async def search_latest_movies(self) -> None:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            soup = await self.scraper.fetch_page(client, HOME)
            for movie in soup.select("div.latest"):
                title = movie.find("strong").get_text(strip=True)
                link = movie.find("a", string="Download Now") or movie.find("a", class_= "green")
                if not link:
                    continue
                self.results.append({"title":title, "movie_url": urljoin(DOMAIN,link["href"])})

    #displays the results
    async def show_results_tui(self, query: str | None = None, year: str | None = None) -> None:

        if query:
            self.parse_search_url(query, year)
            await self.search_movie_url(query, year)
            
            if not self.results:
                print("No movies found.")
                return
        else:
            await self.search_latest_movies()

        # 1. Movie Selection via Fuzzy Finder
        movie_choices = [
            Choice(value=item, name=item["title"]) 
            for item in self.results
        ]
        
        self.selected_movie = await inquirer.fuzzy(
            message="Select the movie (Type to search):",
            choices=movie_choices,
            match_exact=False,
        ).execute_async()

        first_letter = self.selected_movie["title"][0].lower()
        await self.scraper.get_qualities(self.selected_movie["movie_url"], first_letter)
        
        available = {
            "1080p": self.scraper.p1080,
            "720p": self.scraper.p720,
            "480p": self.scraper.p480,
            "360p": self.scraper.p360
        }
        available = {k: v for k, v in available.items() if v}

        if not available:
            print("No qualities available.")
            return

        # 2. Quality Selection (Standard List is cleaner for small sets, but fuzzy works too)
        selected_quality = await inquirer.select(
            message="Select the quality:",
            choices=list(available.keys()),
        ).execute_async()
        
        self.selected_quality_href = available[selected_quality]
        
        available_servers = await self.scraper.get_download_informations(self.selected_quality_href)
        if not available_servers:
            print("No servers available.")
            return

        # 3. Server Selection via Fuzzy Finder
        self.selected_server_url = await inquirer.fuzzy(
            message="Select the server:",
            choices=available_servers,
        ).execute_async()
        
        print(f"Selected Server: {self.selected_server_url}")