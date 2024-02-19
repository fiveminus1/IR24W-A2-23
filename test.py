from bs4 import BeautifulSoup
import requests
import datetime
import scraper
import utils.download
from urllib.parse import urlparse
import json
from collections import defaultdict

#url = 'https://crawler-test.com/links/page_with_external_links'
#url = "https://cs.ics.uci.edu"
#url = "https://ics.uci.edu/~thornton/ics46/Notes/SmartPointers/"
#url = "https://crawler-test.com/redirects/redirect_1"
#url = "https://crawler-test.com/redirects/infinite_redirect"
url = "https://www.ics.uci.edu/"
grab = requests.get(url)

print(urlparse(url), urlparse(grab.url))

soup = BeautifulSoup(grab.text, 'lxml')

#print(soup.get_text())

page_word_counts = defaultdict(int)
common_words = defaultdict(int)


subdomains = defaultdict(int)
redirects = defaultdict(str)
general_analytics = defaultdict(int)

print(scraper.is_redirect(url, grab.url))


# print(page_word_dict)

# print("unique pages:", len(unique_pages))
# print(next_links)





