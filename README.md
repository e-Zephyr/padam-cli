## Disclaimer

padam-cli is an open-source command-line tool that automates browsing and retrieving publicly accessible metadata and links from third-party websites.

This project does not host, store, distribute, stream, or upload any copyrighted media. All content, trademarks, and copyrights belong to their respective owners.

Users are solely responsible for ensuring that their use of this software complies with applicable laws, regulations, and the terms of service of any websites they access.

The author of this project is not responsible for how the software is used and does not encourage copyright infringement or unauthorized distribution of copyrighted material.

This project is provided for educational and research purposes only, without warranty of any kind.

padam-cli is a terminal-based browser for movie metadata and publicly available links.

Features:

* Browse movie listings from supported sources
* View movie metadata
* Select available quality options
* Open or process available media links

padam-cli does not host or redistribute media files.


# Installation(Linux)
Installing **padam-cli** on Linux is simple.
## 1. Install Optional Downloaders
`padam-cli` works out of the box using your default web browser for downloads. However, installing `ffmpeg` and `yt-dlp` gives you more download options.
### Arch Linux
```bash
sudo pacman -S yt-dlp ffmpeg
```
### Ubuntu / Debian
```bash
sudo apt install yt-dlp ffmpeg
```
### Fedora
```bash
sudo dnf install yt-dlp ffmpeg
```
## Which Downloader Should You Use?
You can choose whichever fits your workflow.
* **yt-dlp**
  * ⚡ Very fast startup
  * 🐢 Usually slower download speed
* **ffmpeg**
  * 🐢 Slow startup (takes time to begin downloading)
  * ⚡ Usually the fastest download speed
* **Web Browser**
  * ⚡ Instant startup
  * 🚀 Standard download speed
In reality, download speeds vary depending on the server. Sometimes the web browser can even reach **10+ MB/s**, while `ffmpeg` may spend a few seconds preparing the download. That's why **padam-cli lets you choose whichever downloader you prefer**.
## 2. Install a Media Player
Streaming doesn't require downloading the movie first.
The recommended player is **mpv**.
If you prefer another player (such as VLC), you'll need to copy the generated stream URL and open it manually in your preferred media player.
### Arch Linux
```bash
sudo pacman -S mpv
```
### Ubuntu / Debian
```bash
sudo apt install mpv
```
### Fedora
```bash
sudo dnf install mpv
```
## 3. Clone the Repository
```bash
git clone https://github.com/e-Zephyr/padam-cli.git
cd padam-cli
```
Or download the project as a ZIP file and extract it.
## 4. Run the Installer
```bash
chmod +x install.sh
./install.sh
```
## 5. Add padam-cli to Your PATH
For Fish shell:
```bash
fish_add_path ~/.local/share/bin
```
For Bash or Zsh:
```bash
export PATH="$HOME/.local/share/bin:$PATH"
```
(Add the above line to your shell configuration file if needed.)
## 6. Verify the Installation
```bash
padam-cli -h
```
If the help menu appears, you're ready to use **padam-cli**.


# Installation (Windows)
There are two ways to build **padam-cli** on Windows.
## Option 1: Using uv (Recommended)
If you already have `uv` installed, simply clone the repository and run:
```bash
uv sync
uv run pyinstaller --clean --onefile --name padam-cli main.py
```
The compiled executable will be available in the `dist` folder.
---
## Option 2: Using Python + pip
If you don't use `uv`, first install the required dependencies:
```bash
pip install beautifulsoup4 httpx InquirerPy lxml rich pyinstaller
```
Or install them individually:
```text
beautifulsoup4>=4.15.0
httpx>=0.28.1
InquirerPy>=0.3.4
lxml>=6.1.1
rich>=15.0.0
```
Then build the executable:
```bash
pyinstaller --clean --onefile --name padam-cli main.py
```
After the build finishes, you'll find the executable inside the `dist` folder.


# Usage
```
usage: padam-cli [-h] [-s MOVIE] [-y YEAR] [-p | -d] [{latest}]
Browse, stream, and download Tamil movies.
positional arguments:
  {latest}            Show the latest movies
options:
  -h, --help          Show this help message
  -s, --search MOVIE  Search for a movie
  -y, --year YEAR     Filter by movie year
  -p, --play          Stream the movie
  -d, --download      Download the movie (default)
```
## Search Examples
Search for all movies containing the word **karuppu**:
```bash
padam-cli -s karuppu
```
Search only the **2026** movies containing **karuppu**:
```bash
padam-cli -s karuppu -y 2026
```
Searches are **case-insensitive**, so the following are treated the same:
```bash
padam-cli -s karuppu
padam-cli -s Karuppu
padam-cli -s KARUPPU
```
## Download vs Stream
If you don't specify `-p` or `-d`, **padam-cli downloads the movie by default**.
To stream the movie instead of downloading it, pass the `-p` (or `--play`) option:
```bash
padam-cli -s karuppu -y 2026 -p
```
or
```bash
padam-cli --search karuppu --year 2026 --play
```
This will open the stream directly in **mpv** without downloading the movie.
## Movies That Start With Numbers
Some movie titles begin with numbers, such as **24** or **96**. In these cases, you should also specify the release year to avoid ambiguous results.
```bash
padam-cli -s 24 -y 2016
```
```bash
padam-cli -s 96 -y 2018
```
## Latest Movies
`padam-cli` can also show the latest movies added to the website.
```bash
padam-cli latest
```
This fetches the latest movies available, including newly added OTT releases and theater prints.

# Contribution
Contributions are always welcome—and honestly, they're needed to make **padam-cli** better.
Whether it's fixing bugs, adding new features, improving performance, or even correcting documentation, every contribution helps.
If you're interested, feel free to open an issue, submit a pull request, or share your ideas.
Thanks for checking out **padam-cli**. Hope you'll be part of the project

[for more details see this image](arc-plans/padam-cli.png)