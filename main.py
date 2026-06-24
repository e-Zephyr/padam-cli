from src.argparser import ArgParse
from src.search import Search
from src.media import Media

import asyncio


async def main():
    args = ArgParse()
    search = Search()
    args.parse()

    if args.query:
        await search.show_results_tui(args.query, args.year)
        if args.download:
            Media.download_movie(search.selected_server_url)
        else:
            Media.stream_movie(search.selected_server_url)

    elif args.latest:
        pass
    else:
        raise ValueError

if __name__ == "__main__":
    asyncio.run(main())
