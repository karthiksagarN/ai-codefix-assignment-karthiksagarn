import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import utils

MODEL_NAME = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
_model = None
_tokenizer = None

def load_model():
    """Loads the model and tokenizer."""
    global _model, _tokenizer
    if _model is None:
        print(f"Loading model: {MODEL_NAME}...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            trust_remote_code=True
        )
        utils.set_tokenizer(_tokenizer)
        print("Model loaded successfully.")
    return _model, _tokenizer

def generate_text(prompt: str) -> str:
    """Generates text from the model."""
    model, tokenizer = load_model()
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1024,
        do_sample=False  # Deterministic for code
    )
    
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response
