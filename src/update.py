# src/update.py

from pathlib import Path
import subprocess
import sys

from rich.console import Console

console = Console()

REPO_DIR = Path.home() / ".local" / "share" / "padam-cli"


class Updater:
    @staticmethod
    def update() -> None:
        if not REPO_DIR.exists():
            console.print(f"[red]padam-cli was not found in {REPO_DIR}. Please clone the repository there first.[/red]")
            sys.exit(1)

        if not (REPO_DIR / ".git").exists():
            console.print("[red]Installation is not a Git repository.[/red]")
            sys.exit(1)

        console.print("[cyan]Checking for updates...[/cyan]")

        try:
            subprocess.run(
                ["git", "-C", str(REPO_DIR), "pull", "--ff-only"],
                check=True,
            )
            console.print("[green]padam-cli is up to date.[/green]")

        except subprocess.CalledProcessError:
            console.print("[red]Failed to update padam-cli.[/red]")
            sys.exit(1)