from fastapi import APIRouter
from pydantic import BaseModel
from .recipe_engine import generate_recipe

router = APIRouter()


class RecipeRequest(BaseModel):
    ingredients: str


@router.post("/generate")
def generate(data: RecipeRequest):

    prompt = f"""
Create a recipe using:
{data.ingredients}

Give:
- Ingredients
- All Detailed Steps
"""

    recipe = generate_recipe(prompt)

    return {"recipe": recipe}