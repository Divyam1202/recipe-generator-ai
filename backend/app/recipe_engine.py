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
            max_new_tokens=2048,
            temperature=0.6,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    recipe = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Remove the input prompt from the output if it's included
    if prompt in recipe:
        recipe = recipe.replace(prompt, "", 1)
    
    return recipe.strip()