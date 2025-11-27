from rag import RAGRetriever
import os

def test_rag_retrieval():
    # Ensure we have recipes
    assert os.path.exists("recipes")
    
    retriever = RAGRetriever()
    
    # Test retrieval for SQL injection
    doc = retriever.retrieve("SQL Injection")
    assert "SQL Injection" in doc or "Parameterized Queries" in doc
    
    # Test retrieval for XSS
    doc = retriever.retrieve("Cross-Site Scripting")
    assert "XSS" in doc or "Cross-Site Scripting" in doc
