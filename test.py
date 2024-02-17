from bs4 import BeautifulSoup
import requests
import scraper

url = 'https://www.crawler-test.com/links/page_with_external_links'
grab = requests.get(url)
soup = BeautifulSoup(grab.text, 'lxml')

for link in soup.find_all('a'):
    data = link.get('href')
    if scraper.is_valid(data):
        print(data)

