from src.argparser import ArgParse
from src.search import Search
from src.media import Media

import asyncio
import sys

async def main():
    args = ArgParse()
    search = Search()
    args.parse()

    if args.query:
        await search.show_results_tui(args.query, args.year)
        media = Media(url=search.selected_server_url, title=search.selected_movie["title"])
        media.process(args.download)
    elif args.latest:
        await search.show_results_tui()
        media = Media(url=search.selected_server_url, title=search.selected_movie["title"])
        media.process(args.download)
    else:
        raise ValueError

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Process interrupted by user. Exiting.............")
        sys.exit(0)
