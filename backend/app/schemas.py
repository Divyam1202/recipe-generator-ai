from pydantic import BaseModel
from typing import List, Optional


class RecipeRequest(BaseModel):
    ingredients: str


class RecipeResponse(BaseModel):
    recipe: str


class MessageModel(BaseModel):
    id: int
    type: str  # "user" or "ai"
    content: str


class ConversationModel(BaseModel):
    id: str
    title: str
    messages: List[MessageModel]
    updatedAt: str


class SaveConversationRequest(BaseModel):
    id: str
    title: str
    messages: List[dict]


class DeleteConversationRequest(BaseModel):
    id: str