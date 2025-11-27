import glob
import os
from typing import List
from sentence_transformers import SentenceTransformer, util

class RAGRetriever:
    def __init__(self, recipes_dir: str = "recipes"):
        self.recipes_dir = recipes_dir
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.doc_names = []
        self.embeddings = None
        self._load_documents()

    def _load_documents(self):
        """Loads text files from the recipes directory."""
        filepaths = glob.glob(os.path.join(self.recipes_dir, "*.txt"))
        for filepath in filepaths:
            with open(filepath, 'r') as f:
                content = f.read()
                self.documents.append(content)
                self.doc_names.append(os.path.basename(filepath))
        
        if self.documents:
            self.embeddings = self.model.encode(self.documents, convert_to_tensor=True)

    def retrieve(self, query: str) -> str:
        """Retrieves the most relevant document for the query."""
        if not self.documents:
            return ""
            
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.embeddings, top_k=1)
        
        if hits and hits[0]:
            top_hit = hits[0][0]
            doc_id = top_hit['corpus_id']
            return self.documents[doc_id]
        
        return ""
