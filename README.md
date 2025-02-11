# Favicon Thief

Favicon Thief is a Python script that scrapes and downloads favicons from a list of websites. It extracts favicons from common locations and HTML `<link>` and `<meta>` tags, sorting them by resolution and saving them in an organized directory structure.

## Features
- Automatically detects favicons from `<head>`, `<header>`, and common favicon locations.
- Downloads and saves favicons in order of resolution.
- Supports multiple image formats: `.ico`, `.png`, `.jpg`, `.jpeg`, `.webp`.
- Creates separate directories for each website.
- Uses Python’s `requests` and `BeautifulSoup` for web scraping.
- Works with a list of URLs from a file.

## Installation
Ensure you have UV installed and run `uv sync`

## Usage
1. Create a file named `urls.txt` and list the websites (one per line):

```
https://example.com
https://github.com
https://stackoverflow.com
```

2. Run the script:

```sh
python favicon_thief.py
```

3. The favicons will be saved in the `favicons/` directory, grouped by domain name.

## Directory Structure
```
├── favicon_thief.py
├── urls.txt
├── favicons/
│   ├── example.com/
│   │   ├── 1_192x192.png
│   │   ├── 2_64x64.ico
│   ├── github.com/
│   │   ├── 1_128x128.png
│   ├── stackoverflow.com/
│   │   ├── 1_512x512.png
```

## Notes
- If a URL does not contain "http", the script assumes `https://`.
- If multiple favicons exist, the script saves them all, prioritizing higher resolution images.
- Uses common fallback paths like `/favicon.ico` if no favicon is found in the HTML.