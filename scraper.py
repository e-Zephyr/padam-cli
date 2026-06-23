import asyncio
from typing import Optional
from urllib.parse import urljoin, urlparse
from pathlib import Path
import re

import httpx
from bs4 import BeautifulSoup

from constants import DOMAIN, HEADERS, DOWNLOAD_PATH
from models import Movie, MovieQualities
import subprocess

def download_padam(url: str, output: str):
    subprocess.run(
        [
            "ffmpeg",
            "-i", url,
            "-c", "copy",
            "-y",
            output,
        ],
        check=True,
    )
    
def stream_padam(url: str):
    subprocess.run(["mpv", url])

async def fetch_page(client: httpx.AsyncClient,url: str) -> Optional[BeautifulSoup]:
    try:
        response = await client.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text,"lxml")

    except Exception as exc:
        print(f"Failed to fetch {url}")
        print(exc)
        return None


async def extract_links(client: httpx.AsyncClient,url: str) -> list[tuple[str, str]]:
    soup = await fetch_page(client,url)

    if not soup:
        return []
    
    return [(a.get_text(strip=True) or "[No Text]", a["href"]) for a in soup.find_all("a",href=True)]

async def get_quality_page(movie_url: str) -> list[tuple[str, str]]:
    async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:
        links = await extract_links(client, movie_url)
        original_page = DOMAIN + next(href for _, href in links if "-original-movie" in href)
        if not original_page:
            raise ValueError("Original movie link not found")

        quality_links = await extract_links(client, original_page)
        qualities = MovieQualities()

        for _, href in quality_links:

            match = re.search(
                r"(1080p|720p|360p)",
                href,
                re.IGNORECASE,
            )

            if not match:
                continue

            quality = match.group(1)

            if quality == "1080p":
                qualities.p1080 = href

            elif quality == "720p":
                qualities.p720 = href

            elif quality == "360p":
                qualities.p360 = href
                
        return qualities
    
async def get_download_links(download_page_link: str):
    async with httpx.AsyncClient(follow_redirects=True, timeout=30,headers=HEADERS)as client:
        soup = await fetch_page(client, download_page_link)
        links = [link["href"] for link in soup.select("div.dlink a")]
        
        dlinks = await fetch_page(client, links[0])
        download_links = [link["href"] for link in dlinks.select("div.dlink a")]
        mp_4_links = [link for link in download_links if link.endswith((".mp4", ".m3u8"))]
        return mp_4_links

    
async def get_download_informations(quality_href: str):
    async with httpx.AsyncClient(follow_redirects=True, timeout=30,headers=HEADERS)as client:
        soup = await fetch_page(client, DOMAIN + quality_href)
        download_info_page_link = soup.find("a", class_ = "coral")

        dlinks = await fetch_page(client, DOMAIN + download_info_page_link["href"])
        file_download_page_links = [link["href"] for link in dlinks.select("div.dlink a")]
        movie_download_links = await get_download_links(file_download_page_links[0])
        return movie_download_links
        

async def movie_information(client: httpx.AsyncClient,url: str) -> Optional[Movie]:

    soup = await fetch_page(client,url)

    if not soup:
        return None

    movie_info = soup.find( "ul", class_="movie-info",)

    if not movie_info:
        return None

    metadata = {}

    for li in movie_info.find_all("li"):
        if li.strong and li.span:
            key = li.strong.get_text(strip=True).replace(":", "")
            value = li.span.get_text(strip=True)
            metadata[key] = value

    poster_url = ""
    container = soup.find("div",class_="movie-info-container")

    if container:
        img = container.find("img")

        if img and img.get("src"):
            poster_url = urljoin(url,img["src"])

    return Movie(
        title=metadata.get( "Movie",""),
        director=metadata.get("Director",""),
        starring=metadata.get("Starring",""),
        genres=metadata.get("Genres",""),
        quality=metadata.get("Quality",""),
        language=metadata.get("Language",""),
        rating=metadata.get("Movie Rating",""),
        updated=metadata.get("Last Updated",""),
        poster=poster_url,
        page_url=url,
    )


async def fetch_latest_movies(url: str) -> list[Movie]:

    async with httpx.AsyncClient(follow_redirects=True, timeout=30, headers=HEADERS) as client:

        links = await extract_links(client,url)

        movie_urls = [ DOMAIN + href for text, href in links if text == "Download Now"]

        print(f"Found {len(movie_urls)} movies")

        tasks = [ movie_information(client,movie_url,) for movie_url in movie_urls]

        results = await asyncio.gather( *tasks, return_exceptions=True)

        movies = []

        for result in results:
            if isinstance( result, Movie):
                movies.append(result)

        return movies
    

async def start_scraper(selected_movie:str):
    qualities = await get_quality_page(selected_movie)

    available = {
        "360p": qualities.p360,
        "720p": qualities.p720,
        "1080p": qualities.p1080,
    }

    available = {k: v for k, v in available.items() if v}

    for i, quality in enumerate(available,start=1):
        print(f"[{i}: {quality}]")

    choise = int(input("Select the quality: "))
    selected_quality = list(available.keys())[choise -1]
    selected_quality_url = available[selected_quality]
    available_servers = await get_download_informations(selected_quality_url)

    for index, server in enumerate(available_servers, start=1):
        print(f"[{index}]: {server}")
    selected_server = int(input("Select the server: "))
    movie_url = available_servers[selected_server-1]
    
    watch_option = int(input("[1] : Watch now\n[2] : Download Now\nEnter the option: "))

    if watch_option == 1:
        stream_padam(movie_url)
    else:
        download_file = Path(urlparse(movie_url).path).name
        download_padam(movie_url, Path(DOWNLOAD_PATH).expanduser()/download_file)
        

