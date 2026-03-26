import re

RECIPE_MARKERS = (
    "Now write the complete detailed recipe with ALL sections:",
    "Now write the complete detailed recipe with ALL sections",
    "Now write the recipe:",
)


def strip_prompt_echo(prompt: str, generated_text: str) -> str:
    """Return the recipe text without any echoed prompt scaffolding."""
    recipe = (generated_text or "").strip()
    prompt = (prompt or "").strip()

    if not recipe:
        return ""

    if prompt and recipe.startswith(prompt):
        recipe = recipe[len(prompt):].lstrip()

    for marker in RECIPE_MARKERS:
        if marker in recipe:
            recipe = recipe.rsplit(marker, maxsplit=1)[-1].strip()

    return recipe


def validate_recipe_structure(recipe: str) -> bool:
    """Validate that a generated recipe includes the main required sections."""
    recipe = (recipe or "").strip()
    if len(recipe) < 150:
        return False

    recipe_lower = recipe.lower()
    non_empty_lines = [line.strip() for line in recipe.splitlines() if line.strip()]
    title = non_empty_lines[0] if non_empty_lines else ""

    has_title = bool(title) and not title.startswith(("-", "*", "#")) and len(title) > 3
    has_prep = "prep time" in recipe_lower or re.search(r"\bprep\b", recipe_lower)
    has_cook = "cook time" in recipe_lower or re.search(r"\bcook\b", recipe_lower)
    has_servings = "servings" in recipe_lower or "serves" in recipe_lower
    has_ingredients = "ingredients" in recipe_lower and bool(
        re.search(r"(?m)^\s*[-*]\s+\S", recipe)
    )
    has_steps = bool(re.search(r"(?m)^\s*\d+\.\s+\S", recipe))
    has_serving_tips = (
        "serving tips" in recipe_lower
        or "storage" in recipe_lower
        or "garnish" in recipe_lower
        or "serve" in recipe_lower
    )

    return all(
        (
            has_title,
            has_prep,
            has_cook,
            has_servings,
            has_ingredients,
            has_steps,
            has_serving_tips,
        )
    )
