from googlesearch import search
import os
import logging
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

# Create outputs directory if it doesn't exist
if not os.path.exists('outputs'):
    os.makedirs('outputs')

# Configure logging to output to a log file in the outputs directory
logging.basicConfig(filename='outputs/search_results.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

query = input("Enter query to search: ")
results = int(input("Enter number of results wanted: "))

def is_document(url):
    try:
        # Perform a HEAD request to get the headers
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '').lower()

        # Check if the Content-Type header indicates a common document type
        return any(doc_type in content_type for doc_type in [
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/plain',
            'application/rtf'
        ])
    except Exception as e:
        logging.error(f"Error checking URL {url}: {e}")
        return False

def scrape_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text content from the page
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        logging.error(f"Error scraping URL {url}: {e}")
        return ""

# Perform the search and iterate over results with a progress bar
data = search(query, num_results=results, lang="en", safe=None, advanced=True)
doc_data = {}
content_data = {}
index = 1

for result in tqdm(data, desc="Processing search results"):
    url = result.url
    if is_document(url):
        doc_data[index] = {'type': 'DOC', 'title': result.title, 'url': url, 'description': result.description}
    else:
        content = scrape_content(url)
        content_data[index] = {'type': 'CONTENT', 'title': result.title, 'url': url, 'description': result.description, 'content': content[:200]}  # Store only the first 200 characters
    index += 1

# Combine the dictionaries to print DOCs first and CONTENT second
processed_data = {**doc_data, **content_data}

# Print the processed data
for key, value in processed_data.items():
    logging.info(f"{key}: {value}")
    
print(f"Results have been logged to 'outputs/search_results.log'")

