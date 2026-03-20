from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

_model = None
_tokenizer = None


def load_model():
    global _model, _tokenizer

    if _model is not None:
        return

    print("Loading lightweight model...")

    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    _tokenizer = AutoTokenizer.from_pretrained(model_name)

    _model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="cpu"
    )

    print("Model loaded successfully")


def get_model():
    return _model, _tokenizer