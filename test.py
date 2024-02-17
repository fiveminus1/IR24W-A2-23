from bs4 import BeautifulSoup
import requests
import scraper
import urllib.parse

#url = 'https://crawler-test.com/links/page_with_external_links'
url = "https://ics.uci.edu"
#url = "https://ics.uci.edu/~thornton/ics46/Notes/SmartPointers/"
grab = requests.get(url)
soup = BeautifulSoup(grab.text, 'lxml')

unique_pages = set()
next_links = list()

for a in soup.find_all('a'):
    link = a.get('href')
    if scraper.is_valid(link):
        defragged_link = link.split("#")[0]
        next_links.append(defragged_link)
        unique_pages.add(defragged_link)

print("unique pages:", len(unique_pages))
print(next_links)

