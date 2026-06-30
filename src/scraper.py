import httpx
import re
import sys

from rich.console import Console
from typing import Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.constant import MOVIESDA, HEADERS
from src.logger import Logger
from src.utils import is_valid

console = Console()

class Scraper:
    def __init__(self):
        self.p1080 = None
        self.p720 = None
        self.p480 = None
        self.p360 = None

        self.resolver_current_href = None

    # Fetch the pages
    async def fetch_page(self,client: httpx.AsyncClient, url: str) -> BeautifulSoup | None:

        try:
            response = await client.get(url)
            response.raise_for_status()

            return BeautifulSoup(response.text, "lxml")
        except Exception as e:
            Logger.log(f"Failed to fetch {url}: {e}")
            return None
        
    # Extract the links from pages
    async def extract_links(self, client: httpx.AsyncClient, url: str) -> list[tuple[str,str]]:
        soup = await self.fetch_page(client, url) 

        if not soup:
            console.print("[bold yellow]There is a problem in extracting links[/bold yellow]")
            Logger.log("Soup Not Found: scaraper.py extract_links method")
        return [ ( a.get_text(strip=True) or "[No Text]", a["href"] ) for a in soup.find_all("a", href=True) ]
        Logger.log("Links Extracted sucessfuly")

    #Page navigation
    async def get_pagination_pages(self, client:httpx.AsyncClient, url:str) -> list[str]:
        links = await self.extract_links(client, url)
        pages = {url}

        for text, href in links:
            if text.isdigit():
                pages.add(urljoin(MOVIESDA,href))
        Logger.log(f"{len(pages)} pages found")
        return sorted(pages)
    
    # fetch the qualities from the page
    async def get_qualities(self, movie_url: str, query: str) -> None:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            links = await self.extract_links(client, movie_url)
            original_page = urljoin( MOVIESDA, [href for text, href in links if query.lower() in text.lower() and is_valid(text,href)][0])
            if not original_page:
                console.print(f"[red]There is problem in scaraper[/red]")
                Logger("Movie Link Not Found: in scraper.py get_qualities method")
                Logger(f"this is only founded: {original_page} and Exiting.....")
                sys.exit(0)

            Logger.log(f"Found: {original_page}")

            quality_links = await self.extract_links(client,original_page)

            for _, href in quality_links:
                match = re.search(r"(1080|720|480|360)", href, re.IGNORECASE)

                if not match: continue

                quality = match.group()

                if quality == "1080":
                    self.p1080 = href
                elif quality == "720":
                    self.p720 = href
                elif quality == "480":
                    self.p480 = href
                elif quality == "360":
                    self.p360 = href
    
    # Resolve when something failed in scraping
    async def resolver(self, href: str):
        self.resolver_current_href = href
        async with httpx.AsyncClient(follow_redirects=True, timeout=30,headers=HEADERS)as client:
            links = await self.extract_links(client, urljoin(MOVIESDA, href))
            results = [(text, href) for text, href in links if is_valid(text,href)]
            return results


    #fetch the downloable mp3 or m3u8 urls
    async def get_download_links(self, download_page_link: str) -> list[str]:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30,headers=HEADERS)as client:
            soup = await self.fetch_page(client, download_page_link)
            links = [link["href"] for link in soup.select("div.dlink a")]
            Logger.log(f"Links found : {links} in scraper.py get_dowlnoad_links method")

            dlinks = await self.fetch_page(client, links[0])
            download_links = [link["href"] for link in dlinks.select("div.dlink a")]
            Logger.log(f"download_links = {download_links}")
            
            filtered_download_links = [link for link in download_links if link.endswith((".mp4", ".m3u8")) or "cdn" in link]
            Logger.log(f"filtered = {filtered_download_links}")
            
            return filtered_download_links
        
    #used to crawling to the downloadpage
    async def get_download_informations(self, quality_href) -> list[str]:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            Logger.log(f"processing href : {quality_href} in scraper.py get_download_information method")
            soup = await self.fetch_page(client, urljoin(MOVIESDA, quality_href))
            download_info_page_link = soup.find("a", class_ = "coral")
            
            if download_info_page_link:
                Logger.log(f"download_info_page_link found : {download_info_page_link}")
                dlinks = await self.fetch_page(client, urljoin(MOVIESDA, download_info_page_link["href"]))
            else:
                Logger.log(f"download_info_page_link Not found : {download_info_page_link}")
                Logger.log(f"Now using resolver_current_href: {self.resolver_current_href}")
                dlinks = await self.fetch_page(client, urljoin(MOVIESDA, self.resolver_current_href))

            file_download_page_links = [link["href"] for link in dlinks.select("div.dlink a")]
            movie_download_links = await self.get_download_links(file_download_page_links[0])

            return movie_download_links