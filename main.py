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
        Media.process(args.download,search.selected_movie["title"], search.selected_server_url)
    elif args.latest:
        await search.show_results_tui()
        Media.process(args.download,search.selected_movie["title"], search.selected_server_url)
    else:
        raise ValueError

if __name__ == "__main__":
    asyncio.run(main())
