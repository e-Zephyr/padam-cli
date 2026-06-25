import httpx
import re


from typing import Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.constant import DOMAIN, HEADERS, HOME
from src.logger import Logger

class Scraper:
    def __init__(self):
        self.p1080 = None
        self.p720 = None
        self.p480 = None
        self.p360 = None

    
    async def fetch_page(self,client: httpx.AsyncClient, url: str):

        try:
            response = await client.get(url)
            response.raise_for_status()

            return BeautifulSoup(response.text, "lxml")
        except Exception as e:
            Logger.log(f"Failed to fetch {url}: {e}")
            return None
        

    async def extract_links(self, client: httpx.AsyncClient, url: str):
        soup = await self.fetch_page(client, url) 

        if not soup:return []
        
        return [ ( a.get_text(strip=True) or "[No Text]", a["href"] ) for a in soup.find_all("a", href=True) ]
    
    async def get_pagination_pages(self, client:httpx.AsyncClient, url:str):
        links = await self.extract_links(client, url)

        pages = {url}

        for text, href in links:
            if text.isdigit():
                pages.add(urljoin(DOMAIN,href))

        return sorted(pages)
    
    async def get_qualities(self, movie_url: str, query: str):
        async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            links = await self.extract_links(client, movie_url)
            original_page = urljoin( DOMAIN, [href for text, href in links if query.lower() in text.lower() and href != "#" and href != "/"][0])
            if not original_page:
                Logger("movie link not found")
            Logger.log(f"Found: {original_page}")

            quality_links = await self.extract_links(client,original_page)

            for _, href in quality_links:
                match = re.search(r"(1080p|720p|480p|360p)", href, re.IGNORECASE)

                if not match: continue

                quality = match.group()

                if quality == "1080p":
                    self.p1080 = href
                elif quality == "720p":
                    self.p720 = href
                elif quality == "480p":
                    self.p480 = href
                elif quality == "360p":
                    self.p360 = href

    async def get_download_links(self, download_page_link: str):
        async with httpx.AsyncClient(follow_redirects=True, timeout=30,headers=HEADERS)as client:
            soup = await self.fetch_page(client, download_page_link)
            links = [link["href"] for link in soup.select("div.dlink a")]
            
            dlinks = await self.fetch_page(client, links[0])
            download_links = [link["href"] for link in dlinks.select("div.dlink a")]
            mp_4_links = [link for link in download_links if link.endswith((".mp4", ".m3u8"))]
            return mp_4_links

    async def get_download_informations(self, quality_href):
        async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:
            soup = await self.fetch_page(client, urljoin(DOMAIN, quality_href))
            download_info_page_link = soup.find("a", class_ = "coral")

            dlinks = await self.fetch_page(client, urljoin(DOMAIN, download_info_page_link["href"]))
            file_download_page_links = [link["href"] for link in dlinks.select("div.dlink a")]
            movie_download_links = await self.get_download_links(file_download_page_links[0])

            return movie_download_links