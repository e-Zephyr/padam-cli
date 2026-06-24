from datetime import datetime


class Logger:
    FILE = "logs.txt"

    @classmethod
    def log(cls, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(cls.FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")