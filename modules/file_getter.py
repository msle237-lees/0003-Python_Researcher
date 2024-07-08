import os
import wget
from tqdm import tqdm

# Create outputs directory if it doesn't exist
if not os.path.exists('downloaded_files'):
    os.makedirs('downloaded_files')

class fileGetter:
    def __init__(self):
        self.index = 1
        self.doc_data = {}
        self.content_data = {}
        
    def set_doc_data(self, doc_data):
        self.doc_data = doc_data
    
    def set_content_data(self, content_data):
        self.content_data = content_data
        
    def download_doc_files(self):
        for index, doc in tqdm(self.doc_data.items(), desc="Downloading documents"):
            try:
                wget.download(doc['url'], out=f"downloaded_files/{doc['title']}")
            except Exception as e:
                print(f"Error downloading {doc['title']}: {e}")
                
    def download_content_files(self):
        for index, content in tqdm(self.content_data.items(), desc="Downloading content"):
            try:
                wget.download(content['url'], out=f"downloaded_files/{content['title']}")
            except Exception as e:
                print(f"Error downloading {content['title']}: {e}")
                
    def run(self):
        self.download_doc_files()
        self.download_content_files()
