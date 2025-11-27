import requests
import json
import time

URL = "http://0.0.0.0:8000/local_fix"

samples = [
    {
        "language": "python",
        "cwe": "CWE-89",
        "code": "cursor.execute('SELECT * FROM users WHERE username = ' + username)"
    },
    {
        "language": "python",
        "cwe": "CWE-798",
        "code": "api_key = '12345-abcde-secret'"
    },
    {
        "language": "javascript",
        "cwe": "CWE-79",
        "code": "document.body.innerHTML = '<h1>' + userInput + '</h1>';"
    }
]

def run_tests():
    print("Running local tests against", URL)
    
    for i, sample in enumerate(samples):
        print(f"\n--- Test Case {i+1}: {sample['cwe']} ---")
        start_time = time.time()
        try:
            response = requests.post(URL, json=sample)
            response.raise_for_status()
            data = response.json()
            
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            
            print(json.dumps(data, indent=2))
            print(f"Round-trip Latency: {latency:.2f} ms")
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    run_tests()
