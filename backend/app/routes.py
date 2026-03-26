from fastapi import APIRouter, HTTPException

from .history import clear_all_history, delete_conversation, get_all_conversations, get_conversation, save_conversation
from .prompt_builder import build_generation_context
from .recipe_engine import generate_response
from .schemas import DeleteConversationRequest, RecipeRequest, SaveConversationRequest

router = APIRouter()


@router.post("/generate")
def generate(data: RecipeRequest):
    """Generate a recipe or follow-up response using conversation context."""
    try:
        context = build_generation_context(data.ingredients, data.messages)
        response_text = generate_response(
            chat_messages=context["chat_messages"],
            require_recipe=context["require_recipe"],
        )

        return {"recipe": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")


@router.post("/save-conversation")
def save_conv(data: SaveConversationRequest):
    """Save or update a conversation."""
    try:
        conversation = save_conversation(data.id, data.title, data.messages)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save conversation: {str(e)}")


@router.post("/delete-conversation")
def delete_conv(data: DeleteConversationRequest):
    """Delete a conversation."""
    try:
        success = delete_conversation(data.id)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"success": success}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete conversation: {str(e)}")


@router.get("/history")
def get_history():
    """Get all conversations."""
    try:
        return get_all_conversations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load history: {str(e)}")


@router.get("/history/{conversation_id}")
def get_hist(conversation_id: str):
    """Get a specific conversation."""
    try:
        conversation = get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load conversation: {str(e)}")


@router.post("/clear-history")
def clear_hist():
    """Clear all conversation history."""
    try:
        clear_all_history()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {str(e)}")
