# Write a Python program that takes a URL as a command-line argument, 
# downloads the webpage, and displays the following information:
# The Page Title (without any HTML tags)
# The Page Body Text (only visible text, without HTML tags)
# All the URLs (links) that the page contains


import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {"User-Agent": "Mozilla/5.0"}

def get_page(url):

    try:
        response = requests.get(url, headers=headers)
        return response.text
    except:
        print("Error while fetching page")
        return None


def get_title(soup):

    if soup.title and soup.title.string:
        return soup.title.string.strip()
    else:
        return "No Title Found"


def get_body(soup):

    if not soup.body:
        return "No Body Found"

    text = soup.body.get_text()

    lines = text.split("\n")

    clean_text = ""

    for line in lines:
        line = line.strip()
        if line != "":
            clean_text = clean_text + line + "\n"

    return clean_text


def get_links(soup, base_url):

    links = []

    for tag in soup.find_all("a"):
        href = tag.get("href")

        if href:
            full_url = urljoin(base_url, href)
            links.append(full_url)

    return links


def main():

    # Check command line input
    if len(sys.argv) != 2:
        print("No url found")
        return

    url = sys.argv[1]

    html = get_page(url)

    if html is None:
        return

    soup = BeautifulSoup(html, "html.parser")

    print("Title:\n")
    print(get_title(soup))

    print("\nBody:\n")
    print(get_body(soup))

    print("\n Links:\n")

    links = get_links(soup, url)

    for link in links:
        print(link)



# Run program
if __name__ == "__main__":
    main()