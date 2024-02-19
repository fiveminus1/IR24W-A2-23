import re
import json
import utils.response
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import defaultdict

page_word_counts = defaultdict(int)
common_words = defaultdict(int)
subdomains = defaultdict(int)
redirects = defaultdict(int)
general_analytics = defaultdict(int)

def scraper(url: str, resp: utils.response.Response) -> list:
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    stopwords = set(line.strip() for line in open('stopwords.txt'))

    unique_pages = set()
    next_links = list()
    parsed_url = urlparse(url)

    if resp.status == 200:
        soup = BeautifulSoup(resp.raw_response.content, 'lxml')
        if is_valid(url):
            page_word_counts[url] = count_words(soup) # writes word count of this page to page_word_counts dict (#2 requirement)
            if parsed_url.hostname[0] != "ics" and parsed_url.hostname[1] == "ics": #writes to subdomain dict for urls under ics.uci.edu domain (#4 requirement)
                subdomains[str(parsed_url.hostname)] += 1

        for a in soup.find_all('a'):
            link = a.get('href')
            if is_valid(link):
                defragged_link = link.split("#")[0]
                if defragged_link not in unique_pages:
                    general_analytics["uniques"] += 1 # if site not found in unique pages, adds to general analytics unique page counter (#1 requirement)
                next_links.append(defragged_link)
                unique_pages.add(defragged_link)

    create_analytics_files(page_word_counts, common_words, subdomains, redirects, general_analytics)

    return next_links

def create_analytics_files(page_word_counts: defaultdict, common_words: defaultdict,
                           subdomains: defaultdict, redirects: defaultdict,
                           general_analytics: defaultdict) -> None:
    '''
    Creates the following analytics json files from defaultdicts
    1. Pages and their word counts
    2. Common words
    3. Subdomains
    4. Redirects
    5. General analytics

    :return: Returns a tuple of three paths
    '''
    page_word_counts_path = "analytics/page_word_counts.json" # + str(current_date_time) + ".json"
    common_words_path = "analytics/common_words.json" #+ str(current_date_time) + ".json"
    subdomains_path = "analytics/subdomains.json" #+ str(current_date_time) + ".json"
    redirects_path = "analytics/redirects.json" #+ str(current_date_time) + ".json"
    general_analytics_path = "analytics/general_analytics.json"


    with open(page_word_counts_path, 'w') as pwc_path:
        json.dump(page_word_counts, pwc_path)
    with open(common_words_path, 'w') as cw_path:
        json.dump(common_words, cw_path)
    with open(subdomains_path, 'w') as sub_path:
        json.dump(subdomains, sub_path)
    with open(redirects_path, 'w') as redirects_path:
        json.dump(redirects, redirects_path)
    with open(general_analytics_path, 'w') as ge_path:
        json.dump(general_analytics, ge_path)

def count_words(soup: BeautifulSoup) -> int:
    text = soup.get_text()
    word_count = len(text.split())
    return word_count

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if parsed.hostname not in set(["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|java|txt)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
