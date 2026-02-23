import sys
import requests
from bs4 import BeautifulSoup
import re


# Fetch visible body text from a webpage (used as document content)
def get_bodyText(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Return only body text to avoid HTML noise
    if(soup.body):
        return soup.body.get_text().strip()
    else:
        return " "


# Normalize text → lowercase + keep alphanumeric tokens only
# This acts as basic preprocessing for document comparison
def extract_words(text):
    text = text.lower()
    words = re.findall(r"[a-z0-9]+", text)
    return words;    


# Build term-frequency dictionary (importance of words in document)
def word_frequencies(word):
    freq = {}

    for w in word:
        if w in freq:
            freq[w] += 1
        else:
            freq[w] = 1
    return freq


# Polynomial rolling hash to convert word → 64-bit numeric signature
# Ensures consistent hashing for SimHash computation
def word_hash(word):
    p = 53
    m = 2**64

    hash_value = 0
    power = 1

    for ch in word:
        hash_value += ord(ch) * power
        power = power * p
    
    hash = hash_value % m
    return hash


# Compute SimHash fingerprint (64-bit) for a document
# Weighted by term frequency → preserves semantic importance
def simHash(freq_dict):
    vector = [0] * 64

    for w, count in freq_dict.items():
        h = word_hash(w)

        # Add/Subtract weight based on hash bits
        for i in range(64):
            bit = (h >> i)&1

            if bit == 1:
                vector[i] += count
            else:
                vector[i] -= count
    
    # Convert sign vector → binary fingerprint
    fingerprint = 0
    for i in range(64):
        if vector[i] >= 0 :
            fingerprint = fingerprint | (1 << i)
    return fingerprint


# Count matching bits between two SimHash fingerprints
# Higher common bits → higher document similarity
def common_bits(h1, h2):
    count = 0

    for i in range(64):
        if((h1 >> i)& 1) == ((h2 >> i)& 1):
            count += 1

    return count



# Ensure two URLs are provided for comparison
if len(sys.argv) < 3:
    print("No url found")

url1= sys.argv[1]
url2 = sys.argv[2]


# ---- Document Similarity Pipeline ----
# 1. Fetch webpage body text
# 2. Normalize and tokenize text
# 3. Compute term frequency
# 4. Generate SimHash fingerprint
# 5. Compare fingerprints using bit similarity


text1 = get_bodyText(url1)
text2 = get_bodyText(url2)
# print(text[:500])

words1 = extract_words(text1)
words2 = extract_words(text2)
# print(words[:100])

freq_dict1 = word_frequencies(words1)
freq_dict2 = word_frequencies(words2)
# print(freq_dict)

# for word, count in freq_dict.items():
#     h = word_hash(word)
#     print(h)

doc_hash1 = simHash(freq_dict1)
doc_hash2 = simHash(freq_dict2)

# print("SimHash 1:", doc_hash1)
# print("SimHash 2:", doc_hash2)

print("Common bits: ", common_bits(doc_hash1, doc_hash2))