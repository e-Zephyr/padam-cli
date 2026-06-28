import argparse


class ArgParse:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="padam-cli",
            description="Browse, stream and download Tamil movies."
        )


        parser.add_argument(
            "--update",
            action="store_true",
            help="Update padam-cli"
        )

        # latest command
        parser.add_argument(
            "command",
            nargs="?",
            choices=["latest", "dubbed"],
            help="Show latest or dubbed movies"
        )

        # search
        parser.add_argument(
            "-s", "--search",
            metavar="MOVIE",
            help="Search movie"
        )

        # year
        parser.add_argument(
            "-y", "--year",
            type=str,
            metavar="YEAR",
            help="Movie year"
        )

        # play/download
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "-p", "--play",
            action="store_true",
            help="Stream movie"
        )

        group.add_argument(
            "-d", "--download",
            action="store_true",
            help="Download movie (default)"
        )

        self.parser = parser

    def parse(self):
        args = self.parser.parse_args()

        self.query = args.search
        self.year = args.year
        self.latest = args.command == "latest"
        self.dubbed = args.command == "dubbed"
        self.update = args.update

        # Download is the default
        self.download = not args.play

        return self