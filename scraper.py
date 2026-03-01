import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {"User-Agent": "Mozilla/5.0"}

def normalize_url(url):
    if not url.startswith("http"):
        url = "https://" + url
    return url

def download_page(url):
    try:
        r = requests.get(url, headers=headers)
        return r.text
    except:
        print("Error downloading page")
        sys.exit()

def extract_title(soup):
    if soup.title:
        print(soup.title.text.strip())
    else:
        print("No Title Found")
    print()

def extract_body(soup):
    if soup.body:
        text = soup.body.get_text(" ", strip=True)
        print(text)
    print()


def extract_links(base_url, soup):
    visited = set()
    for link in soup.select("a[href]"):
        href = link.get("href")

        current = urljoin(base_url, href)
        if current not in visited:
            print(current)
            visited.add(current)


def main():
    if len(sys.argv) < 2:
        print("Please provide valid URL")
        return

    input_url = sys.argv[1]
    url = normalize_url(input_url)
    html = download_page(url)
    soup = BeautifulSoup(html, "html.parser")
    extract_title(soup)
    extract_body(soup)
    extract_links(url, soup)

main()