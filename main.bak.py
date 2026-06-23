import httpx
import ffmpeg
from bs4 import BeautifulSoup
from typing import Optional

DOMAIN = "https://moviesda32.com"

def movie_information(url: str) -> Optional[dict]:
    try:
        response = httpx.get(url, follow_redirects = True)
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    movie_info_list = soup.find("ul", class_="movie-info")

    if not movie_info_list:
        print("Could not find movie information on this page.")
        return None

    movie_data = {}

    for li in movie_info_list.find_all("li"):
        if li.strong and li.span:
            key = li.strong.get_text(strip=True).replace(":", "")
            value = li.span.get_text(strip=True)
            movie_data[key] = value

    return movie_data


def download_padam(url:str, output: str):
    (
        ffmpeg
        .input(url)
        .output(output, c="copy")
        .overwrite_output()
        .run()
    )

def get_final_links(url:str):
    links = page_links(url)
    download_link1 = links[1][1]
    download_link2 = links[2][1]
     
    return (download_link1, download_link2)

def get_server_links(url: str):
    links = page_links(DOMAIN + url)
    server1 = page_links(links[1][1])[1][1]
    server2 = page_links(links[1][1])[2][1]
    return(server1,server2)

def get_qualites(url: str):
    new_url = DOMAIN + url
    links = page_links(new_url)

    _1080p = links[1][1]
    _720p = links[2][1]
    _360p = links[3][1]

    return (_1080p,_720p,_360p)


def get_moview_orginal_link(url: str):
    links = page_links(url)
    return links[1][1]

def get_downloads(url: str):
    links = page_links(url)
    download_links = [link[1] for link in links if link[0] == "Download Now"]
    for index, link in enumerate(download_links,1):
        print(f"[{index}]:{link}")

    choise = int(input("Enter the index to open next page: "))
    new_url = DOMAIN + download_links[choise-1]

    movie_original_link = get_moview_orginal_link(new_url)

    qualities = get_qualites(movie_original_link)

    link_for_server_page = page_links(DOMAIN + qualities[2])[1][1]
    servers = get_server_links(link_for_server_page)
    link_for_download = get_final_links(servers[0])
    print(link_for_download)
    download_padam(link_for_download[0], "output.mp4")

def preview_page(url: str):
    print(f"Fetching: {url}...\n" + "-"*40)
    
    try:
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        print(f"PAGE TITLE: {soup.title.string if soup.title else 'No Title Found'}\n")
        print("PAGE CONTENT SUMMARY:")
        text_content = soup.get_text(separator="\n", strip=True)
        print(text_content)
        print("-"*40)
        print("DISCOVERED LINKS:")
        # 4. Extract and print numbered links
        for index, a in enumerate(soup.find_all("a", href=True), 1):
            link_text = a.get_text(strip=True) or "[No Text]"
            link_href = a["href"]
            print(f"[{index}] {link_text} -> ({link_href})")
            
    except Exception as e:
        print(f"Error fetching the page: {e}")

def page_links(url: str):
    try:
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        links = [[a.get_text(strip=True) or "[No Text]",a["href"]] for a in soup.find_all("a", href=True)]
        return links
    except Exception as e:
        print(f"Error fetching the page: {e}")



def main():
    target = "https://moviesda32.com/home.html"
    get_downloads(target)

if __name__ == "__main__":
    main()