__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import polars as pl
import uuid
import chromadb

class Portfolio:
    def __init__(self, file_path="resources/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pl.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstorage')
        self.collection = self.chroma_client.get_or_create_collection(name='portfolio')

    def load_portfolio(self):
        if not self.collection.count():
            for techstack, link in self.data.iter_rows():
                self.collection.add(
                    documents=techstack,
                    metadatas={"links": link},
                    ids = [str(uuid.uuid4())]
                    )
    
    def query_links(self, skills):
        return self.collection.query(
            query_texts=skills,
            n_results=2
        ).get('metadatas', [])