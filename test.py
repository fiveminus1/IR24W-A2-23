from bs4 import BeautifulSoup
import requests
import datetime
import scraper
import urllib.parse
import json
from collections import defaultdict

#url = 'https://crawler-test.com/links/page_with_external_links'
url = "https://ics.uci.edu"
#url = "https://ics.uci.edu/~thornton/ics46/Notes/SmartPointers/"
grab = requests.get(url)
soup = BeautifulSoup(grab.text, 'lxml')


page_word_counts = defaultdict(int)
common_words = defaultdict(int)
subdomains = defaultdict(int)
redirects = defaultdict(int)
general_analytics = defaultdict(int)

page_word_counts["ics.uci.edu"] = 1001
common_words["the"] = 500
subdomains["ics.uci.edu"] = 402
redirects["ics.uci.edu"] = 5

subdomains["ics.uci.edu"] = 405

scraper.create_analytics_files(page_word_counts, common_words, subdomains, redirects, general_analytics)



# if scraper.is_valid(url):
#     page_and_counters.write(str(url) + ' ' + str(scraper.count_words(soup)))
#     page_word_dict[url] = scraper.count_words(soup)
#
# for a in soup.find_all('a'):
#     link = a.get('href')
#
#     if scraper.is_valid(link):
#         defragged_link = link.split("#")[0]
#         next_links.append(defragged_link)
#         unique_pages.add(defragged_link)


# print(page_word_dict)

# print("unique pages:", len(unique_pages))
# print(next_links)





