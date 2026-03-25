from fastapi import APIRouter
from pydantic import BaseModel
from .recipe_engine import generate_recipe
from .history import save_conversation, delete_conversation, get_all_conversations, clear_all_history, get_conversation
from .schemas import SaveConversationRequest, DeleteConversationRequest

router = APIRouter()


class RecipeRequest(BaseModel):
    ingredients: str


@router.post("/generate")
def generate(data: RecipeRequest):

    prompt = f"""Create a detailed and delicious recipe using the following ingredients or requirements:
{data.ingredients}

Please provide:
1. Recipe Title
2. Prep Time and Cook Time
3. Servings
4. Detailed Ingredients List with quantities
5. Step-by-step Cooking Instructions (at least 5-7 detailed steps)
6. Tips for serving and variations

Format the recipe clearly and make the instructions easy to follow."""

    recipe = generate_recipe(prompt)
    
    # Clean up the recipe by removing the original prompt if present
    if "Create a detailed" in recipe:
        recipe = recipe.split("Create a detailed")[1]
    
    return {"recipe": recipe.strip()}


@router.post("/save-conversation")
def save_conv(data: SaveConversationRequest):
    """Save or update a conversation."""
    conversation = save_conversation(data.id, data.title, data.messages)
    return conversation


@router.post("/delete-conversation")
def delete_conv(data: DeleteConversationRequest):
    """Delete a conversation."""
    success = delete_conversation(data.id)
    return {"success": success}


@router.get("/history")
def get_history():
    """Get all conversations."""
    return get_all_conversations()


@router.get("/history/{conversation_id}")
def get_hist(conversation_id: str):
    """Get a specific conversation."""
    conversation = get_conversation(conversation_id)
    if not conversation:
        return {"error": "Conversation not found"}, 404
    return conversation


@router.post("/clear-history")
def clear_hist():
    """Clear all conversation history."""
    clear_all_history()
    return {"success": True}