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

class fileSearcher:
    def __init__(self):
        # Perform the search and iterate over results with a progress bar
        self.doc_data = {}
        self.content_data = {}
        self.index = 1
    
    def is_document(self, url):
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
        
    def scrape_content(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text content from the page
            return soup.get_text(separator=' ', strip=True)
        except Exception as e:
            logging.error(f"Error scraping URL {url}: {e}")
            return ""
    
    def run(self, query, results):
        self.data = search(query, num_results=results, lang="en", safe=None, advanced=True)
        for result in tqdm(self.data, desc="Processing search results"):
            url = result.url
            if self.is_document(url):
                self.doc_data[self.index] = {'type': 'DOC', 'title': result.title, 'url': url, 'description': result.description}
            else:
                content = self.scrape_content(url)
                self.content_data[self.index] = {'type': 'CONTENT', 'title': result.title, 'url': url, 'description': result.description, 'content': content[:200]}  # Store only the first 200 characters
            self.index += 1
   
        print(f"Results have been logged to 'outputs/search_results.log'")
        return self.doc_data, self.content_data

if __name__ == '__main__':
    m = fileSearcher()
    
    query = input("Enter query to search: ")
    results = int(input("Enter number of results wanted: "))

    doc_data, content_data = m.run(query, results)
