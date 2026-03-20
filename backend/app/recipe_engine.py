from .model_loader import get_model
import torch


def generate_recipe(prompt: str):

    model, tokenizer = get_model()

    if model is None or tokenizer is None:
        raise Exception("Model not loaded")

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1000,
            temperature=0.7,
            do_sample=True
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)