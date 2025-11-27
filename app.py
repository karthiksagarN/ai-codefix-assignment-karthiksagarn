import time
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

import model_loader
import rag
import prompt_template
import utils

# Initialize RAG
rag_retriever = rag.RAGRetriever()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    model_loader.load_model()
    yield

app = FastAPI(lifespan=lifespan)

class FixRequest(BaseModel):
    language: str
    cwe: str
    code: str

class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int

class FixResponse(BaseModel):
    fixed_code: str
    diff: str
    explanation: str
    model_used: str
    token_usage: TokenUsage
    latency_ms: float

def parse_response(response_text: str):
    """Parses the LLM response to extract fixed code, diff, and explanation."""
    fixed_code = ""
    diff = ""
    explanation = ""
    
    # Simple parsing based on delimiters
    parts = re.split(r'---(FIXED_CODE|DIFF|EXPLANATION)---\n', response_text)
    
    current_section = None
    for part in parts:
        if part in ['FIXED_CODE', 'DIFF', 'EXPLANATION']:
            current_section = part
        elif current_section == 'FIXED_CODE':
            fixed_code = part.strip()
        elif current_section == 'DIFF':
            diff = part.strip()
        elif current_section == 'EXPLANATION':
            explanation = part.strip()
            
    return fixed_code, diff, explanation

@app.post("/local_fix", response_model=FixResponse)
async def local_fix(request: FixRequest):
    start_time = time.time()
    
    # 1. RAG Retrieval
    context = rag_retriever.retrieve(request.cwe)
    
    # 2. Prompt Assembly
    prompt = prompt_template.build_prompt(
        request.language,
        request.cwe,
        request.code,
        context
    )
    
    # 3. Model Generation
    response_text = model_loader.generate_text(prompt)
    
    # 4. Output Parsing
    fixed_code, diff, explanation = parse_response(response_text)
    
    # Fallback diff generation if model fails to provide it or provides invalid one
    if not diff:
        diff = utils.generate_diff(request.code, fixed_code)
        
    # 5. Metrics
    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000
    
    input_tokens = utils.count_tokens(prompt)
    output_tokens = utils.count_tokens(response_text)
    
    # 6. Logging
    utils.log_metrics(
        request.cwe,
        model_loader.MODEL_NAME,
        input_tokens,
        output_tokens,
        latency_ms
    )
    
    return FixResponse(
        fixed_code=fixed_code,
        diff=diff,
        explanation=explanation,
        model_used=model_loader.MODEL_NAME,
        token_usage=TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens
        ),
        latency_ms=latency_ms
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
