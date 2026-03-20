import torch
from .model_loader import model, tokenizer


def generate_recipe(prompt: str):

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=250,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    result = tokenizer.decode(output[0], skip_special_tokens=True)

    return result