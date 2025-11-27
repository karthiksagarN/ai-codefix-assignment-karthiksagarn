# AI Code Fix Microservice

A local LLM-powered code remediation microservice that uses RAG to fix security vulnerabilities.

## Architecture

```ascii
+-------------+      +-----------------+      +------------------+
|   Client    | ---> |    FastAPI      | ---> |   Local LLM      |
| (Requests)  |      |   (app.py)      |      | (Qwen2.5-Coder)  |
+-------------+      +--------+--------+      +------------------+
                              |
                              v
                     +-----------------+
                     |  RAG Retriever  | <--- recipes/*.txt
                     |    (rag.py)     |
                     +-----------------+
```

## Setup Steps

1. **Prerequisites**: Python 3.10+, pip, and optionally a GPU.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Download Model**: The application will automatically download `Qwen/Qwen2.5-Coder-1.5B-Instruct` and `all-MiniLM-L6-v2` on the first run.

## How to Run

### Run Locally
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Run with Docker
```bash
docker build -t ai-codefix .
docker run -p 8000:8000 ai-codefix
```

## How to Run Tests

### Unit Tests
```bash
pytest
```

### Integration Test
Start the server first, then run:
```bash
python test_local.py
```

## How RAG Works
The service loads security guidelines from `recipes/*.txt`. When a request comes in, it uses cosine similarity to find the most relevant guideline based on the CWE or vulnerability description and injects it into the prompt.

## Example Request

**POST** `/local_fix`

```json
{
  "language": "python",
  "cwe": "CWE-89",
  "code": "<vulnerable code snippet>"
}
```

## Example Response

```json
{
  "fixed_code": ".....",
  "diff": "...",
  "explanation": "......",
  "model_used": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
  "token_usage": {
    "input_tokens": 0,
    "output_tokens": 0
  },
  "latency_ms": 0
}
```

## Performance Notes
- **Latency**: Depends on hardware. GPU inference is significantly faster than CPU.
- **Memory**: Requires ~4GB RAM for the 1.5B model.

## Folder Structure
- `app.py`: Main FastAPI application
- `model_loader.py`: LLM loading and inference
- `rag.py`: RAG implementation
- `prompt_template.py`: Prompt construction
- `utils.py`: Helper functions
- `recipes/`: Security guidelines
- `tests/`: Unit tests
- `test_local.py`: Integration test script

## EnterSoft Assignment
Name: Karthik Sagar Nallagula
Email: karthik.sagar@gmail.com
LinkedIn: https://linkedin.com/in/karthik-sagar-nallagula
Portfolio: https://karthiknallagula.com
Github: https://github.com/karthiksagarn# ai-codefix-assignment-karthiksagarn
