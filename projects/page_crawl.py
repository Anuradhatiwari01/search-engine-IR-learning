# Write a Python program that takes a URL as a command-line argument, 
# downloads the webpage, and displays the following information:
# The Page Title (without any HTML tags)
# The Page Body Text (only visible text, without HTML tags)
# All the URLs (links) that the page contains


import sys
import requests
from bs4 import BeautifulSoup

# Simple user agent to avoid block requests 
headers = {"User-Agent": "Mozilla/5.0"}

# Get HTML of webpage
def get_page(url):
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Could not open page. Status code:", response.status_code)
        return None

    return response.text


# Get page title
def get_title(soup):
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    else:
        return "No Title Found"


# Get visible body text
def get_body(soup):
    if not soup.body:
        return "No Body Found"

    text = soup.body.get_text()
    lines = text.split("\n")

    clean_text = ""
    for line in lines:
        line = line.strip()
        if line != "":
            clean_text += line + "\n"
    return clean_text



# Get all links
def get_links(soup):
    links = []

    for tag in soup.find_all("a"):
        href = tag.get("href")

        # ignore empty links
        if href and href != "#":
            links.append(href)

    return links



# Check command line input
if len(sys.argv) != 2:
    print("Wrong url given!! Retry.")
    sys.exit(1)

url = sys.argv[1]
html = get_page(url)

if html is None:
    sys.exit(1)

soup = BeautifulSoup(html, "html.parser")

print("Page Title: ")
print(get_title(soup))
print()

print("Body Text (First 800 chars): ")
body_text = get_body(soup)
print(body_text[:1000])

print()

print("Links: ")
links = get_links(soup)

if len(links) == 0:
    print("No links found")
else:
    for link in links:
        print(link)
