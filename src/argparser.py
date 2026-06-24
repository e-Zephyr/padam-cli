import sys


class ArgParse:
    def __init__(self):
        self.query = None
        self.year = None
        self.latest = False
        self.download = True

    def help(self):
        print(
            """
padam-cli

Usage:
padam-cli latest
padam-cli --search <movie> [year]

Options:
-P, --play       Stream movie
-D, --download   Download movie (default)
-h, --help       Show help

Examples:
padam-cli latest
padam-cli --search Leo
padam-cli -D --search Leo 2023
padam-cli -P --search Zombie
"""
        )

    def parse(self):
        command = sys.argv[1:]

        if not command:
            self.help()
            sys.exit(0)

        if "-h" in command or "--help" in command:
            self.help()
            sys.exit(0)

        if "-P" in command:
            self.download = False

        if "-D" in command:
            self.download = True

        if "--search" in command:
            index = command.index("--search")

            args = command[index + 1 :]

            if not args:
                raise ValueError("Movie name is required.")

            # Check if last argument is a year
            if args[-1].isdigit():
                if len(args[-1]) != 4:
                    raise ValueError(f"Invalid year: {args[-1]}")

                self.year = args[-1]
                self.query = " ".join(args[:-1])

                if not self.query:
                    raise ValueError("Movie name is required.")
            else:
                self.query = " ".join(args)

        elif command[0] == "latest":
            self.latest = True

        else:
            raise ValueError(
                f"Unknown command: {' '.join(command)}\n"
                "Usage:\n"
                "  padam-cli latest\n"
                "  padam-cli --search <movie> [year]"
            )

        return self