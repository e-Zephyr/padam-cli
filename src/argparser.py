import sys


class ArgParse:
    def __init__(self):
        self.query = None
        self.year = None
        self.latest = False
        self.download = True

    def parse(self):
        command = sys.argv[1:]

        if not command:
            raise ValueError(
                "No command provided.\n"
                "Usage:\n"
                "  padam-cli latest\n"
                "  padam-cli --search <movie> [year]"
                "  padam-cli -P for play by default Download if not given"
                "  padam-cli -D for download"
            )
        
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