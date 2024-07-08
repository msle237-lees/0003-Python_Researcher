from modules.file_searcher import fileSearcher
from modules.file_getter import fileGetter


class app:
    def __init__(self):
        self.searcher = fileSearcher()
        self.getter = fileGetter()

        # Define the doc_data and content_data variables
        self.doc_data = {}
        self.content_data = {}
        
        self.query = ""
        self.results_num = 0
        
    def get_query_and_results_num(self):
        self.query = input("Enter a search query: ")
        self.results_num = int(input("Enter the number of results to process: "))
        
    def run(self):
        self.get_query_and_results_num()
        self.doc_data, self.content_data = self.searcher.run(self.query, self.results_num)
        self.getter.set_doc_data(self.doc_data)
        self.getter.set_content_data(self.content_data)
        self.getter.run()
        
if __name__ == '__main__':
    app = app()
    app.run()