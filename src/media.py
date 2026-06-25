import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from rich.console import Console
from src.constant import DOWNLOAD_PATH

console = Console()

class Media:
    def __init__(self, url: str, title: str | None = None, download_dir: str = DOWNLOAD_PATH):
        self.url = url
        self.title = title
        self.download_dir = Path(download_dir).expanduser()
        self.filename = self._generate_filename()
        self.output_path = self.download_dir / self.filename

    def _generate_filename(self) -> str:
        try:
            query = parse_qs(urlparse(self.url).query)
            if "path" in query:
                return Path(query["path"][0]).name
        except Exception:
            pass

        name = Path(urlparse(self.url).path).name
        if "." in name: return name
        if self.title: return f"{self.title}.mp4"
        return "movie.mp4"

    def download(self):
        cmd = [
            "ffmpeg",
            "-i", self.url, 
            "-c", "copy", 
            "-y", 
            str(self.output_path)
        ]
        console.print(f"[bold cyan]Download started. Downloading in path {self.output_path}[/bold cyan]")
        with console.status(f"[bold cyan]Downloading:[/bold cyan] {self.filename}", spinner="dots"):
            subprocess.run(cmd, check=True)
        console.print(f"[bold green]✓ Complete:[/bold green] {self.output_path}")

    def stream(self):
        console.print("[bold cyan]Starting stream with mpv...[/bold cyan]")
        subprocess.run(["mpv", self.url], check=True)

    def process(self, should_download: bool):
        if should_download:
            self.download()
        else:
            self.stream()