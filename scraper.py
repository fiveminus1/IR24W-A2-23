import re
import json
import utils.response
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import defaultdict

stopwords = set(line.strip() for line in open('stopwords.txt'))
page_word_counts = defaultdict(int)
common_words = defaultdict(int)
subdomains = defaultdict(int)
redirects = defaultdict(str)
visited_pages = defaultdict(int)
general_analytics = defaultdict(int)


def scraper(url: str, resp: utils.response.Response) -> list:
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to
    # get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content


    unique_pages = set()
    next_links = list()
    parsed_url = urlparse(resp.url)

    if resp.status == 200 and not is_crawler_trap(resp.url, resp): #check that content is greater than 10 (not a dead link)
        soup = BeautifulSoup(resp.raw_response.content, 'lxml')

        if is_redirect(url, resp.url): # detects if the provided url was a redirect and if so, adds to redirects defaultdict (#5 behavior)
            redirects[url] = resp.url

        if is_valid(resp.url):
            word_count = count_words(soup, common_words, stopwords) # writes word count of this page to page_word_counts dict (#2 report) and writes common words (#3 report)
            page_word_counts[url] = word_count

            if word_count > general_analytics["longest_page_word_count"]: #if this page's word count is greater than the longest page, set it in general analytics (#2 report)
                general_analytics["longest_page_word_count"] = word_count

            if parsed_url.hostname[0] != "ics" and parsed_url.hostname[1] == "ics": #writes to subdomain dict for urls under ics.uci.edu domain (#4 report)
                subdomains[str(parsed_url.hostname)] += 1

        for a in soup.find_all('a'):
            link = a.get('href')
            if is_valid(link):
                defragged_link = link.split("#")[0]
                if defragged_link not in unique_pages:
                    general_analytics["uniques"] += 1 # if site not found in unique pages, adds to general analytics unique page counter (#1 report)
                next_links.append(defragged_link)
                unique_pages.add(defragged_link)
                visited_pages[defragged_link] += 1
                print(next_links)

    create_analytics_files(page_word_counts, common_words, subdomains, redirects, visited_pages, general_analytics)
    print("Current general analytics: " + str(general_analytics))
    return next_links


def is_crawler_trap(url, resp) -> bool:
    year_pattern = r'\b(?:19|20)\d{2}\b'
    if redirects[url] == resp.url: # if a page has already been redirected to the same page, we can skip it and/or assume it's a trap
        return True
    if visited_pages[url] > 10: # test threshold; if a page has already been visited over 10 times, we can stop visiting it and/or assume it's a trap
        return True
    for path in urlparse(url).path.split("/"): #check if contains date, event, ml datasets for possible traps
        if path == "ml" or path == "events":
            return True
        if re.search(year_pattern, path):
            return True

    return False


def create_analytics_files(page_word_counts: defaultdict, common_words: defaultdict,
                           subdomains: defaultdict, redirects: defaultdict, visited_pages: defaultdict,
                           general_analytics: defaultdict) -> None:
    '''
    Creates the following analytics json files from defaultdicts
    1. Pages and their word counts
    2. Common words
    3. Subdomains
    4. Redirects
    5. Pages visited
    6. General analytics

    :return: Returns a tuple of three paths
    '''
    page_word_counts_path = "analytics/page_word_counts.json" # + str(current_date_time) + ".json"
    common_words_path = "analytics/common_words.json" #+ str(current_date_time) + ".json"
    subdomains_path = "analytics/subdomains.json" #+ str(current_date_time) + ".json"
    redirects_path = "analytics/redirects.json" #+ str(current_date_time) + ".json"
    visited_pages_path = "analytics/visited_pages.json"
    general_analytics_path = "analytics/general_analytics.json"

    with open(page_word_counts_path, 'w') as pwc_path:
        json.dump(page_word_counts, pwc_path)
    with open(common_words_path, 'w') as cw_path:
        json.dump(common_words, cw_path)
    with open(subdomains_path, 'w') as sub_path:
        json.dump(subdomains, sub_path)
    with open(redirects_path, 'w') as re_path:
        json.dump(redirects, re_path)
    with open(visited_pages_path, 'w') as vp_path:
        json.dump(visited_pages, vp_path)
    with open(general_analytics_path, 'w') as ge_path:
        json.dump(general_analytics, ge_path)

def count_words(soup: BeautifulSoup, common_words: defaultdict, stopwords: set) -> int:
    '''
    Counts the number of words in a BeautifulSoup object and modifies the common_words defaultdict

    :param soup: BeautifulSoup object constructed from a website
    :return: Returns total number of words
    '''
    text = soup.get_text().split() # O(n) to split
    for word in text: # Counts each word in the text and adds it to common_words dict (#3 report)
        if word not in stopwords:
            common_words[word] += 1

    word_count = len(text)
    return word_count


def is_redirect(url: str, resp_url: str):
    parsed_url = urlparse(url)
    parsed_grabbed_url = urlparse(resp_url)
    return parsed_url.scheme != parsed_grabbed_url.scheme or parsed_url.netloc.lstrip("www.") != parsed_grabbed_url.netloc.lstrip("www.") or parsed_url.path.rstrip(
        '/') != parsed_grabbed_url.path.rstrip('/')

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
