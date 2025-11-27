import csv
import difflib
import os
import time
from datetime import datetime

# Global tokenizer placeholder (will be set by model_loader)
TOKENIZER = None

def set_tokenizer(tokenizer):
    """Sets the global tokenizer."""
    global TOKENIZER
    TOKENIZER = tokenizer

def count_tokens(text: str) -> int:
    """Counts tokens using the loaded tokenizer."""
    if TOKENIZER:
        return len(TOKENIZER.encode(text))
    return 0

def generate_diff(original: str, fixed: str) -> str:
    """Generates a unified diff between original and fixed code."""
    original_lines = original.splitlines(keepends=True)
    fixed_lines = fixed.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        fixed_lines,
        fromfile='original',
        tofile='fixed',
        lineterm=''
    )
    return ''.join(diff)

def log_metrics(cwe: str, model: str, input_tokens: int, output_tokens: int, latency_ms: float):
    """Appends structured logs to metrics.csv."""
    file_exists = os.path.isfile('metrics.csv')
    
    with open('metrics.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'cwe', 'model', 'input_tokens', 'output_tokens', 'latency_ms'])
        
        writer.writerow([
            datetime.now().isoformat(),
            cwe,
            model,
            input_tokens,
            output_tokens,
            latency_ms
        ])
