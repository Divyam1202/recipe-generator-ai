import logging
import os

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)

_model = None
_tokenizer = None


def load_model():
    global _model, _tokenizer

    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    model_name = os.getenv("RECIPE_MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    logger.info("Loading model: %s", model_name)

    _tokenizer = AutoTokenizer.from_pretrained(model_name)

    _model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        device_map="cpu"
    )

    logger.info("Model loaded successfully")
    return _model, _tokenizer


def get_model():
    if _model is None or _tokenizer is None:
        return load_model()
    return _model, _tokenizer
