import os
from io import BytesIO
from urllib.parse import urlparse, urljoin

import requests
from PIL import Image
from bs4 import BeautifulSoup

# Read URLs from file
urls = None
with open("urls.txt") as f:
    urls = [line.strip() for line in f.readlines() if line.strip()]

assert len(urls) > 0, "The URLs list is empty!"

# Directory to save favicons
base_output_dir = "favicons"
os.makedirs(base_output_dir, exist_ok=True)

# Common fallback favicon locations
COMMON_FAVICON_PATHS = [
    "/favicon.ico",
    "/favicon.png",
    "/apple-touch-icon.png",
    "/apple-touch-icon-precomposed.png"
]

# Valid image file extensions
VALID_IMAGE_EXTENSIONS = (".ico", ".png", ".jpg", ".jpeg", ".webp")


def fetch_html(url):
    """Fetches HTML content of a website."""
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_favicon_links(html, base_url):
    """Parses HTML to find favicon images from <head> and <header>."""
    soup = BeautifulSoup(html, "html.parser")
    favicons = set()

    # Extract <link> and <meta> tags that contain favicon-related images
    for tag in soup.find_all(["link", "meta"]):
        href = tag.get("href") or tag.get("content")
        if href and any(ext in href.lower() for ext in VALID_IMAGE_EXTENSIONS):
            favicons.add(urljoin(base_url, href))

    # Extract <img> tags from <head> and <header> sections
    for section in ["head", "header"]:
        for img in soup.find_all("img", src=True):
            img_url = img["src"]
            if any(ext in img_url.lower() for ext in VALID_IMAGE_EXTENSIONS):
                favicons.add(urljoin(base_url, img_url))

    return favicons


def check_common_favicons(base_url):
    """Checks common locations for favicons."""
    return [urljoin(base_url, path) for path in COMMON_FAVICON_PATHS]


def get_image_resolution(image_data):
    """Returns the resolution of an image from binary data."""
    try:
        image = Image.open(BytesIO(image_data))
        return image.size  # (width, height)
    except Exception:
        return (0, 0)  # Default if it fails


def download_favicons(url):
    """Downloads all favicons from a given website and sorts them by resolution."""
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.replace("www.", "")
    output_dir = os.path.join(base_output_dir, domain_name)
    os.makedirs(output_dir, exist_ok=True)

    # Try fetching HTML and extracting favicon links
    html = fetch_html(url)
    favicon_urls = set()

    if html:
        favicon_urls.update(extract_favicon_links(html, url))

    # Add common fallback paths
    favicon_urls.update(check_common_favicons(url))

    # Download favicons and save them
    favicon_data = []
    for favicon_url in favicon_urls:
        try:
            response = requests.get(favicon_url, stream=True, timeout=5)
            if response.status_code == 200:
                image_data = response.content
                resolution = get_image_resolution(image_data)
                favicon_data.append((favicon_url, image_data, resolution))
        except requests.RequestException:
            continue

    if not favicon_data:
        print(f"No favicons found for {url}")
        return

    # Sort by highest resolution
    favicon_data.sort(key=lambda x: x[2][0] * x[2][1], reverse=True)

    # Save favicons
    for idx, (favicon_url, image_data, resolution) in enumerate(favicon_data):
        ext = os.path.splitext(favicon_url)[-1].lower()
        if ext not in VALID_IMAGE_EXTENSIONS:
            ext = ".png"  # Default to PNG if unknown

        filename = f"{idx + 1}_{resolution[0]}x{resolution[1]}{ext}"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "wb") as f:
            f.write(image_data)

        print(f"Saved: {favicon_url} -> {file_path}")


# Process each URL
for url in urls:
    if "http" not in url:
        url = "https://" + url
    download_favicons(url)

print("Favicon fetching completed.")
