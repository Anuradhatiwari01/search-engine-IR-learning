# Extend your previous Python web‑processing project to implement document similarity detection using the SimHash technique.
# Your program must perform the following tasks:
# Word Frequency Calculation
# Extract the body text of a webpage.
# Count the frequency of every word in the document body.
# Implement a 64‑bit hash function for each word using the polynomial rolling hash method. 
# Use the word hashes and their frequencies to compute a 64‑bit SimHash fingerprint of the document.
# Similarity Comparison Between Two Documents



import sys
import requests
from bs4 import BeautifulSoup
import re


# Get body text from webpage
def get_body_text(url):

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch:", url)
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    if soup.body:
        return soup.body.get_text().strip()
    else:
        return ""



def extract_words(text):
    text = text.lower()
    words = re.findall(r"[a-z0-9]+", text)

    return words



# Count word frequencies
def word_frequencies(words):

    freq = {}
    for w in words:
        if w in freq:
            freq[w] += 1
        else:
            freq[w] = 1
    return freq



# Rolling hash for a word (64-bit)
def word_hash(word):

    p = 53
    m = 2**64
    hash_value = 0
    power = 1
    for ch in word:
        hash_value += ord(ch) * power
        power = power * p
    return hash_value % m


# Compute Simhash fingerprint
def simhash(freq_dict):

    array = [0] * 64
    for word, count in freq_dict.items():

        h = word_hash(word)
        for i in range(64):
            bit = (h >> i) & 1
            if bit == 1:
                array[i] += count
            else:
                array[i] -= count

    fingerprint = 0
    for i in range(64):
        if array[i] >= 0:
            fingerprint |= (1 << i)
    return fingerprint


# Count common bits
def common_bits(h1, h2):

    count = 0
    for i in range(64):
        if ((h1 >> i) & 1) == ((h2 >> i) & 1):
            count += 1

    return count


if len(sys.argv) < 3:
    print("Wrong input given")
    sys.exit(1)

url1 = sys.argv[1]
url2 = sys.argv[2]


print("Fetching pages...")

text1 = get_bodyText(url1)
text2 = get_bodyText(url2)
print("Length of page 1:", len(text1))
print("Length of page 2:", len(text2))


words1 = extract_words(text1)
words2 = extract_words(text2)
print("Total words page 1:", len(words1))
print("Total words page 2:", len(words2))


freq1 = word_frequencies(words1)
freq2 = word_frequencies(words2)


hash1 = simhash(freq1)
hash2 = simhash(freq2)
print("Simhash 1:", hash1)
print("Simhash 2:", hash2)


common = common_bits(hash1, hash2)
print("Common bits:", common)
similarity = (common / 64) * 100
print("Similarity: {:.2f}%".format(similarity))