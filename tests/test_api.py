from fastapi.testclient import TestClient
from app import app
import pytest

client = TestClient(app)

def test_local_fix_endpoint():
    payload = {
        "language": "python",
        "cwe": "CWE-89",
        "code": "cursor.execute('SELECT * FROM users WHERE username = ' + username)"
    }
    
    # Mocking model generation to avoid loading heavy model during quick tests
    # In a real scenario, we might want integration tests that actually run the model
    # or mock the model_loader.generate_text function.
    # For this assignment, we'll assume the model loads or we mock it.
    # Here I will mock the generate_text function to speed up tests and avoid memory issues
    
    import model_loader
    original_generate = model_loader.generate_text
    
    def mock_generate(prompt):
        return """---FIXED_CODE---
cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

---DIFF---
- cursor.execute('SELECT * FROM users WHERE username = ' + username)
+ cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

---EXPLANATION---
Use parameterized queries.
"""
    model_loader.generate_text = mock_generate
    
    try:
        response = client.post("/local_fix", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert "fixed_code" in data
        assert "diff" in data
        assert "explanation" in data
        assert "model_used" in data
        assert "token_usage" in data
        assert "latency_ms" in data
    finally:
        model_loader.generate_text = original_generate
