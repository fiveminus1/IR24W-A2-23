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
url = "https://httpstat.us/200"
grab = requests.get(url)

soup = BeautifulSoup(grab.text, 'lxml')
=
print(soup.get_text())

page_word_counts = defaultdict(int)
common_words = defaultdict(int)
#common_words = OrderedDict(sorted())

subdomains = defaultdict(int)
redirects = defaultdict(str)
general_analytics = defaultdict(int)

# if scraper.is_redirect(url, grab.url):
#     redirects[url] = grab.url
#
# if redirects[url] == grab.url:
#     print("lol")

# word_count = scraper.count_words(soup, common_words, stopwords)
# if word_count > general_analytics["longest_page_word_count"]:  # if this page's word count is greater than the longest page, set it in general analytics (#2 report)
#     general_analytics["longest_page_word_count"] = word_count
# sorted_common_words = sorted(common_words.items(), key = lambda x:x[1], reverse=True)
# print(sorted_common_words)
# print(str(general_analytics))




# page_word_counts["ics.uci.edu"] = 1001
# common_words["the"] = 500
# subdomains["ics.uci.edu"] = 402
# redirects["ics.uci.edu"] = 5
#
# subdomains["ics.uci.edu"] = 405

# scraper.create_analytics_files(page_word_counts, common_words, subdomains, redirects, general_analytics)



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





