import logging
from typing import Dict, List, Optional

import torch

from .model_loader import get_model
from .recipe_utils import strip_prompt_echo, validate_recipe_structure

logger = logging.getLogger(__name__)
MIN_GENERAL_RESPONSE_LENGTH = 5


def _render_fallback_chat_prompt(chat_messages: List[Dict[str, str]]) -> str:
    lines = []
    for message in chat_messages:
        role = message["role"].capitalize()
        lines.append(f"{role}: {message['content']}")
    lines.append("Assistant:")
    return "\n\n".join(lines)


def _tokenize_request(tokenizer, prompt: Optional[str], chat_messages: Optional[List[Dict[str, str]]]):
    rendered_prompt = prompt or ""

    if chat_messages:
        try:
            input_ids = tokenizer.apply_chat_template(
                chat_messages,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt",
            )
            return {"input_ids": input_ids}, tokenizer.decode(input_ids[0], skip_special_tokens=False)
        except Exception as exc:
            logger.warning("Falling back to plain-text prompt rendering: %s", exc)
            rendered_prompt = _render_fallback_chat_prompt(chat_messages)

    inputs = tokenizer(rendered_prompt, return_tensors="pt")
    return inputs, rendered_prompt


def _is_valid_response(response_text: str, require_recipe: bool) -> bool:
    if require_recipe:
        return len(response_text) >= 150 and validate_recipe_structure(response_text)
    return len(response_text.strip()) >= MIN_GENERAL_RESPONSE_LENGTH


def generate_response(
    prompt: Optional[str] = None,
    chat_messages: Optional[List[Dict[str, str]]] = None,
    require_recipe: bool = True,
    max_retries: int = 2,
):
    """Generate either a recipe or a conversational follow-up based on the request mode."""

    for attempt in range(max_retries):
        try:
            model, tokenizer = get_model()

            if model is None or tokenizer is None:
                raise RuntimeError("Model or tokenizer failed to load")

            if tokenizer.pad_token_id is None and tokenizer.eos_token_id is not None:
                tokenizer.pad_token = tokenizer.eos_token

            inputs, rendered_prompt = _tokenize_request(tokenizer, prompt, chat_messages)
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
            response_text = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
            response_text = strip_prompt_echo(rendered_prompt, response_text)

            if not _is_valid_response(response_text, require_recipe):
                logger.warning(
                    "Attempt %s: Response failed validation (require_recipe=%s, length=%s)",
                    attempt + 1,
                    require_recipe,
                    len(response_text),
                )
                if attempt == max_retries - 1:
                    if require_recipe:
                        raise ValueError("Recipe missing required sections or content")
                    raise ValueError("Model generated insufficient content")
                continue

            logger.info("Response generated successfully on attempt %s", attempt + 1)
            return response_text
            
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
    
    raise RuntimeError("Response generation failed after all retry attempts")


def generate_recipe(prompt: str, max_retries: int = 2):
    """Backward-compatible recipe generation wrapper."""
    return generate_response(prompt=prompt, require_recipe=True, max_retries=max_retries)
