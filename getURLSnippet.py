import requests
from bs4 import BeautifulSoup


def fetch_and_parse_url(url): #NOT USED SINCE IT PREVENTS ERRORS FROM BEING RECORDED, IT HANDLES PDFs ANYWAYS
    try:
        response = requests.get(url)
        content_type = response.headers.get('Content-Type')

        # Check if the content is HTML or a PDF
        if 'application/pdf' in content_type:
            print(f"Skipping PDF file: {url}")
            return None  # Skipping PDF content
        elif 'text/html' in content_type:
            response.encoding = 'utf-8'  # Ensure UTF-8 encoding for HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup  # Return BeautifulSoup object for HTML
        else:
            print(f"Unknown content type: {content_type} for URL: {url}")
            return None  # Skipping unknown content types

    except Exception as e:
        print(f"Error fetching or parsing content from {url}: {e}")
        return None



def scrape_og_stuff(url):
    og_stuff = {
        "og_title": "",
        "og_description": "",
        "og_image": "",
        "meta_description": "",
        "error": ""
    }
    
    try:
        # Fetch the webpage content
        response = requests.get(url, timeout=10)  # Set timeout to avoid hanging indefinitely

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
        
        #soup = fetch_and_parse_url(url)#skips pdfs properly, but stops the handling of errors

        # Extract Open Graph data
        og_title = soup.find("meta", property="og:title")
        og_description = soup.find("meta", property="og:description")
        og_image = soup.find("meta", property="og:image")
        meta_description = soup.find("meta", attrs={"name": "description"})

        # Populate the dictionary with available data
        og_stuff["og_title"] = og_title['content'] if og_title else ""
        og_stuff["og_description"] = og_description['content'] if og_description else ""
        og_stuff["og_image"] = og_image['content'] if og_image else ""
        og_stuff["meta_description"] = meta_description['content'] if meta_description else ""

    except requests.ConnectionError as e:
        og_stuff["error"] = f"ConnectionError: {str(e)}"
    except requests.Timeout as e:
        og_stuff["error"] = f"TimeoutError: {str(e)}"
    except Exception as e:
        og_stuff["error"] = f"GeneralError: {str(e)}"

    return og_stuff