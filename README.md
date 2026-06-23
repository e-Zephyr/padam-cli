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


## Installation
```bash
git clone https://github.com/e-Zephyr/padam-cli.git
cd padam-cli

# Install dependencies
uv sync
```
Run directly:
```bash
uv run main.py
```
Build a standalone binary:
```bash
uv run pyinstaller --clean --onefile --name padam-cli main.py
```
The binary will be generated in:
```text
dist/padam-cli
```
Run it:
```bash
./dist/padam-cli
```
