import model_loader
import pytest

# This test might be slow as it loads the model
# We can mark it to be skipped if needed, but requirements say "test model loading"
def test_model_loading():
    model, tokenizer = model_loader.load_model()
    assert model is not None
    assert tokenizer is not None
