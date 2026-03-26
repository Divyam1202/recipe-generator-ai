from pydantic import BaseModel, Field
from typing import List


class MessageModel(BaseModel):
    id: int
    type: str  # "user" or "ai"
    content: str


class RecipeRequest(BaseModel):
    ingredients: str = Field(..., min_length=1, max_length=2000, description="Ingredients for the recipe")
    messages: List[MessageModel] = Field(default_factory=list)


class RecipeResponse(BaseModel):
    recipe: str


class ConversationModel(BaseModel):
    id: str
    title: str
    messages: List[MessageModel]
    updatedAt: str


class SaveConversationRequest(BaseModel):
    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=500)
    messages: List[MessageModel]


class DeleteConversationRequest(BaseModel):
    id: str = Field(..., min_length=1)
