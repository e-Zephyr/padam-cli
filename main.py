from src.argparser import ArgParse
from src.search import Search
from src.media import Media
from rich.console import Console
from src.update import Updater

import asyncio
import sys

console = Console()
async def main():
    args = ArgParse()
    search = Search()
    
    args.parse()

    if args.query:
        await search.show_results_tui(args.query, args.year, args.latest, args.dubbed)
        media = Media(url=search.selected_server_url, title=search.selected_movie["title"])
        media.process(args.download)
    elif args.latest:
        await search.show_results_tui(args.query, args.year, args.latest, args.dubbed)
        media = Media(url=search.selected_server_url, title=search.selected_movie["title"])
        media.process(args.download)
    elif args.dubbed:
        await search.show_results_tui(args.query, args.year, args.latest, args.dubbed)
        media = Media(url=search.selected_server_url, title=search.selected_movie["title"])
        media.process(args.download)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("[bold red]\n[!] Process interrupted by user. Exiting.............[/bold red]")
        sys.exit(0)
