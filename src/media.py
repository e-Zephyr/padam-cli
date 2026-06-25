import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from src.constant import DOWNLOAD_PATH

class Media:
    @staticmethod
    def get_filename(url: str, title: str | None = None) -> str:
        try:
            query = parse_qs(urlparse(url).query)
            if "path" in query:
                return Path(query["path"][0]).name
        except Exception:
            pass

        filename = Path(urlparse(url).path).name
        
        if "." in filename:
            return filename
        if title:
            return f"{title}.mp4"
            
        return "movie.mp4"

    @staticmethod
    def download_movie(url: str, title: str | None = None):
        filename = Media.get_filename(url, title)
        output = Path(DOWNLOAD_PATH).expanduser() / filename
        subprocess.run(["ffmpeg", "-i", url, "-c", "copy", "-y", str(output)], check=True)

    @staticmethod
    def stream_movie(url: str):
        subprocess.run(["mpv", url], check=True)

    @staticmethod
    def start(download:bool,title:str, url:str):
        if download:
            Media.download_movie(url, title)
        else:
            Media.stream_movie(url)