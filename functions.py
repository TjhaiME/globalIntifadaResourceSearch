from pathlib import Path
import os

#config_path = Path("zeroshot.cfg")
def test_open_file(file_path):
    # Check if the file is readable
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print("Config file read successfully.")
    except Exception as e:
        print(f"Failed to read config file: {e}")
        print("Current working directory:", os.getcwd())


def scriptRelativePathToFullPath(scriptLocalPath):
    # Get the directory of the current script
    script_dir = Path(__file__).parent

    # Build the full path to the config file
    config_path = script_dir / scriptLocalPath#so we can use the script from any working directory
    #relative file paths in python are relative to working directory IN THE COMMAND LINE, Not in the script
    return config_path


import json

def loadJson(myfilename):

    with open(myfilename) as f:
        d = json.load(f)
        return d
    



####################################################
#             URL to filename bijection
#####################################################

import urllib.parse

# Characters not allowed in file names
FORBIDDEN_CHARS = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '%']

# Encode URL to a safe filename
def url_to_filename(url):
    # Parse the URL to ensure it's valid and escape certain characters
    url_encoded = urllib.parse.quote(url, safe='')
    
    # Replace forbidden characters with their percent-encoded form if needed
    filename = url_encoded
    for char in FORBIDDEN_CHARS:
        filename = filename.replace(char, f'%{ord(char):02X}')
    
    return filename

# Decode filename back to the original URL
def filename_to_url(filename):
    # Replace percent-encoded forbidden characters with the original ones
    for char in FORBIDDEN_CHARS:
        filename = filename.replace(f'%{ord(char):02X}', char)
    
    # Decode percent-encoded characters to their original form
    url = urllib.parse.unquote(filename)
    
    return url

# Example usage
# url = "https://example.com/path/to/resource?query=param&value=10"
# filename = url_to_filename(url)
# print(f"Original URL: {url}")
# print(f"Converted to filename: {filename}")

# # Convert back to URL
# original_url = filename_to_url(filename)
# print(f"Converted back to URL: {original_url}")



from urllib.parse import urlparse
def get_url_mainText(url):
    # Sample URL
    #url = "https://www.example.com/page/subpage?query=123"

    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the domain (netloc)
    domain = parsed_url.netloc

    # Split the domain by dots
    domain_parts = domain.split('.')

    # Extract the middle part (without the 'www' and TLD)
    if domain_parts[0] == "www":
        middle_part = domain_parts[1]
    else:
        middle_part = domain_parts[0]

    return middle_part  # Output: example





####################################################
#      News scraping
####################################################
#From: https://www.newscatcherapi.com/blog/python-web-scraping-libraries-to-mine-news-data


from bs4 import BeautifulSoup
def scrape_news(url):
    from newspaper import Article
    failed_file = scriptRelativePathToFullPath('failed_urls.txt')
    try:
        article = Article(url)
        article.download()
        article.parse()
        soup = BeautifulSoup(article.html, 'html.parser')
        anchor_elements = soup.find_all('a')
        dict_array = [{'text': element.get_text(), 'href': element.get('href')} for element in anchor_elements]
        article = {
            "title": str(article.title),
            "text": str(article.text),
            "authors": article.authors,
            "published_date": str(article.publish_date),
            "top_image": str(article.top_image),
            "videos": article.movies,
            "keywords": article.keywords,
            "summary": str(article.summary),
            "anchors" : dict_array
        }
        return article
    except Exception as e:  # Catching all exceptions (including timeouts)
        print(f"Failed to scrape {url}: {e}")
        # Save the failed URL to a file
        with open(failed_file, 'a') as f:
            f.write(f"Failed: {url}, Error: {e}\n")
        return {}
#print(get_anchors(url))

# import newspaper

# from bs4 import BeautifulSoup

def scrape_news_OLD(url):
    from newspaper import Article
    article = Article(url=url, language='en')
    article.download()
    article.parse()
    
    #print("article keys = ", article.keys())
    soup = BeautifulSoup(article.html, 'html.parser')
    anchor_elements = soup.find_all('a')

    article ={
        "title": str(article.title),
        "text": str(article.text),
        "authors": article.authors,
        "published_date": str(article.publish_date),
        "top_image": str(article.top_image),
        "videos": article.movies,
        "keywords": article.keywords,
        "summary": str(article.summary),
        "anchors" : anchor_elements
    }
    #print("html = ", article["html"])
    return article






##################################################