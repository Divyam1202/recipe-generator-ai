import logging
import os
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

try:
    from peft import AutoPeftModelForCausalLM
except ImportError:  # pragma: no cover - compatibility fallback
    AutoPeftModelForCausalLM = None

logger = logging.getLogger(__name__)

_model = None
_tokenizer = None
LOCAL_MODEL_DIR = Path(__file__).resolve().parents[2] / "models" / "finalmodel"


def _resolve_model_source() -> str:
    explicit_source = os.getenv("RECIPE_MODEL_SOURCE")
    if explicit_source:
        return explicit_source

    if LOCAL_MODEL_DIR.exists():
        return str(LOCAL_MODEL_DIR)

    return os.getenv("RECIPE_MODEL_NAME", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")


def load_model():
    global _model, _tokenizer

    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    model_source = _resolve_model_source()
    logger.info("Loading model from: %s", model_source)

    _tokenizer = AutoTokenizer.from_pretrained(model_source)

    if Path(model_source).is_dir() and (Path(model_source) / "adapter_config.json").exists():
        if AutoPeftModelForCausalLM is None:
            raise RuntimeError(
                "The configured local adapter model requires a PEFT version with "
                "AutoPeftModelForCausalLM support."
            )
        _model = AutoPeftModelForCausalLM.from_pretrained(
            model_source,
            torch_dtype=torch.float32,
            device_map="cpu",
        )
    else:
        _model = AutoModelForCausalLM.from_pretrained(
            model_source,
            torch_dtype=torch.float32,
            device_map="cpu",
        )

    if _tokenizer.pad_token is None and _tokenizer.eos_token is not None:
        _tokenizer.pad_token = _tokenizer.eos_token

    logger.info("Model loaded successfully")
    return _model, _tokenizer


def get_model():
    if _model is None or _tokenizer is None:
        return load_model()
    return _model, _tokenizer
