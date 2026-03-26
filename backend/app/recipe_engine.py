import logging
import torch

from .model_loader import get_model
from .recipe_utils import strip_prompt_echo, validate_recipe_structure

logger = logging.getLogger(__name__)


def generate_recipe(prompt: str, max_retries: int = 2):
    """
    Generate a recipe from the provided prompt.
    
    Args:
        prompt: The prompt describing the recipe request
        max_retries: Number of retry attempts on failure
        
    Returns:
        Generated recipe string with all required sections
        
    Raises:
        Exception: If model fails to generate valid recipe after retries
    """
    
    for attempt in range(max_retries):
        try:
            model, tokenizer = get_model()

            if model is None or tokenizer is None:
                raise RuntimeError("Model or tokenizer failed to load")

            inputs = tokenizer(prompt, return_tensors="pt")
            inputs = {key: value.to(model.device) for key, value in inputs.items()}

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=2500,
                    temperature=0.4,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.2,
                    length_penalty=0.8,
                    num_beams=1,
                    no_repeat_ngram_size=2,
                    early_stopping=True
                )

            prompt_token_count = inputs["input_ids"].shape[1]
            generated_tokens = outputs[0][prompt_token_count:]
            recipe = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
            recipe = strip_prompt_echo(prompt, recipe)
            
            # Validate recipe has actual content
            if not recipe or len(recipe) < 150:
                logger.warning(f"Attempt {attempt + 1}: Generated recipe too short ({len(recipe)} chars)")
                if attempt == max_retries - 1:
                    raise ValueError("Model generated insufficient content")
                continue
            
            # Validate recipe structure
            if not validate_recipe_structure(recipe):
                logger.warning(f"Attempt {attempt + 1}: Recipe missing required sections")
                if attempt == max_retries - 1:
                    raise ValueError("Recipe missing required sections (Title, Times, Servings, Ingredients, Steps, Tips)")
                continue
            
            logger.info(f"Recipe generated successfully on attempt {attempt + 1}")
            return recipe
            
        except torch.cuda.OutOfMemoryError:
            logger.error(f"Attempt {attempt + 1}: GPU out of memory")
            if attempt == max_retries - 1:
                raise RuntimeError("GPU out of memory - recipe generation failed")
        except RuntimeError as e:
            logger.error(f"Attempt {attempt + 1}: Runtime error: {str(e)}")
            if attempt == max_retries - 1:
                raise
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}: Unexpected error: {str(e)}")
            if attempt == max_retries - 1:
                raise RuntimeError(f"Failed to generate recipe: {str(e)}")
    
    raise RuntimeError("Recipe generation failed after all retry attempts")
