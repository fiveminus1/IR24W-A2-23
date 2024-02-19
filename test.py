from bs4 import BeautifulSoup
import requests
import datetime
import scraper
import urllib.parse

#url = 'https://crawler-test.com/links/page_with_external_links'
url = "https://ics.uci.edu"
#url = "https://ics.uci.edu/~thornton/ics46/Notes/SmartPointers/"
grab = requests.get(url)
soup = BeautifulSoup(grab.text, 'lxml')

page_and_counters = open("analytics/page_and_wordcounters.txt", 'w')
page_word_dict = dict()
unique_pages = set()
next_links = list()

dt = datetime.datetime.now()
current_date_time = dt.strftime("%m-%d %H.%m")


print(current_date_time)

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





