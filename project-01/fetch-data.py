import sys 
import requests
from bs4 import BeautifulSoup
import re


# Ensure a root URL is provided via command line
if len(sys.argv) < 2:
    print("NO URL given")
    sys.exit(1)

# Read root URL from command line argument
url = sys.argv[1]

# Send HTTP GET request to fetch webpage content
response = requests.get(url)

# Extract raw HTML from response
html_content = response.text

# Parse HTML using BeautifulSoup for structured extraction
soup = BeautifulSoup(html_content, "html.parser")


# Extract and display page title (useful for indexing / metadata)
print(soup.title.text)


# Extract visible body text (basic content retrieval for IR processing)
print(soup.body.get_text().strip())


# Find all hyperlink tags for link graph / crawling
links = soup.find_all("a")

# Extract and print href attributes (outgoing links from root URL)
for i in links:
    print(i.get("href"))



# ---- Project Flow Summary ----
# 1. Accept root URL from command line
# 2. Fetch webpage using HTTP GET
# 3. Parse HTML structure
# 4. Extract page title (metadata)
# 5. Extract body text (content retrieval)
# 6. Extract hyperlinks (for crawling / link analysis)
