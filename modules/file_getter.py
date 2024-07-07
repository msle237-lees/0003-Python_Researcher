import os
import sys
import requests
from tqdm import tqdm

class fileGetter:
    def __init__(self):
        self.index = 1
        self.doc_data = {}
        self.content_data = {}
    
    def set_doc_data(self, doc_data):
        self.doc_data = doc_data
        self.index = len(doc_data) + 1
    
    def download_file(self, url, output_dir):
        try:
            response = requests.get(url)
            # Get the filename from the URL
            filename = url.split('/')[-1]
            # Save the file to the specified output directory
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(response.content)
            return filename
        except Exception as e:
            print(f"Error downloading file from URL {url}: {e}")
            return None
        
    def run(self, doc_data, output_dir):
        for index, doc in tqdm(doc_data.items(), desc="Downloading files"):
            url = doc['url']
            filename = self.download_file(url, output_dir)
            if filename:
                self.doc_data[self.index] = {'type': 'DOC', 'title': doc['title'], 'url': url, 'filename': filename, 'description': doc['description']}
                index += 1
        return self.doc_data
    

if __name__ == "__main__":
    getter = fileGetter()
    doc_data = {
        1: {'type': 'DOC', 'title': 'Document 1', 'url': 'http://example.com/doc1', 'description': 'This is the first document'},
        2: {'type': 'DOC', 'title': 'Document 2', 'url': 'http://example.com/doc2', 'description': 'This is the second document'}
    }
    getter.run(doc_data, 'outputs')