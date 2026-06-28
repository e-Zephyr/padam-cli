from src.constant import DOMAIN , HEADERS, HOME
from urllib.parse import urljoin
from src.scraper import Scraper
from InquirerPy import inquirer
from InquirerPy.base import Choice
from src.logger import Logger

from rich.console import Console
import sys
import httpx

console = Console()
class Search:
    def __init__(self):
        self.search_url = None
        
        self.results = []
        self.selected_movie = None

        self.available_qualities = None
        self.selected_quality_href = None
        
        self.available_servers = None
        self.selected_server_url = None
        

        self.scraper = Scraper()

    #parse the base url for search
    def parse_search_url(self, query:str, year: str | None=None) -> None:
        if year:
            self.search_url = urljoin(DOMAIN,f"/tamil-{year}-movies/")
        else:
            href = query[0].lower()
            self.search_url = urljoin(DOMAIN ,f"/tamil-movies/{href}/")
        Logger.log(f"Searching url: {self.search_url}")

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
                        Logger.log(f" Found : [{movie["title"]}] --> {movie["movie_url"]}")

            return self.results
        
    # used only for fetch latest added movies
    async def search_latest_movies(self) -> None:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            soup = await self.scraper.fetch_page(client, HOME)
            for movie in soup.select("div.latest"):
                title = movie.find("strong").get_text(strip=True)
                link = movie.find("a", string="Download Now") or movie.find("a", class_= "green")
                if not link:
                    continue
                self.results.append({"title":title, "movie_url": urljoin(DOMAIN,link["href"])})
            Logger.log(f"{len(self.results)} of Latest movies found")

    # Determine movie source
    async def determine_movie_source(self, query:str | None = None, year:str | None = None) -> None:
        if query:
            self.parse_search_url(query, year)
            await self.search_movie_url(query, year)
            
            if not self.results:
                console.print(f"[bold yellow] No movies found. Exiting....... [/bold yellow]")
                Logger.log("No movies found. Exiting.......")
                sys.exit(0)
                return
        else:
            await self.search_latest_movies()

    # Prompt movie selection
    async def prompt_movie_selection(self) -> None:
        movie_choices = [
            Choice(value=item, name=item["title"]) 
            for item in self.results
        ]
        
        self.selected_movie = await inquirer.fuzzy(
            message="Select the movie (Type to search):",
            choices=movie_choices,
            match_exact=False,
        ).execute_async()
        Logger.log(f"Selected Movie : {self.selected_movie}")

    # Load available servers
    async def load_available_qualities(self) -> None:
        first_letter = self.selected_movie["title"][0].lower()
        await self.scraper.get_qualities(self.selected_movie["movie_url"], first_letter)
        
        available = {
            "1080p": self.scraper.p1080,
            "720p": self.scraper.p720,
            "480p": self.scraper.p480,
            "360p": self.scraper.p360
        }

        self.available_qualities = {k: v for k, v in available.items() if v}

    # Retrieve download servers
    async def retrieve_download_servers(self) -> None:
        if self.available_qualities:
            selected_quality = await inquirer.select(
                message="Select the quality:",
                choices=list(self.available_qualities.keys()),
            ).execute_async()
            
            self.selected_quality_href = self.available_qualities[selected_quality]
            self.available_servers = await self.scraper.get_download_informations(self.selected_quality_href)
        else:
            resolver_results = await self.scraper.resolver(self.selected_movie["movie_url"])
            while True:
                if any("download" in text.lower() for text, _ in resolver_results): break

                selected = await inquirer.select(
                    message="Select and click Enter:",
                    choices=[text for text, _ in resolver_results]
                ).execute_async()

                next_href = dict(resolver_results)[selected]
                Logger.log(f"Moving to next --> {next_href}" )
                resolver_results = await self.scraper.resolver(next_href)
            self.available_servers = await self.scraper.get_download_informations(self.scraper.resolver_current_href)

    # Load and select servers
    async def prompt_server_selection(self) -> None:
        if not self.available_servers:
            console.print("[bold red]No servers available.[/bold red]")
            Logger.log("No server found. Exiting....")
            sys.exit(0)

        self.selected_server_url = await inquirer.fuzzy(
            message="Select the server:",
            choices=self.available_servers,
        ).execute_async()
        
        console.print(f"[green]Selected Server: {self.selected_server_url}[/green]")

    # displays the results
    async def show_results_tui(self, query: str | None = None, year: str | None = None) -> None:

        # 1. Determine movie source
        await self.determine_movie_source(query, year)

        # 2. Prompt movie selection
        await self.prompt_movie_selection()

        # 3. Load available video qualities
        await self.load_available_qualities()

        # 4. Retrieve download servers
        await self.retrieve_download_servers()  

        # 5. Validate and select download server
        await self.prompt_server_selection()