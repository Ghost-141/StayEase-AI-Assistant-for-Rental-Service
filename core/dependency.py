from typing import Annotated
from fastapi import Depends
from services.chat_service import ChatService

def get_chat_service() -> ChatService:
    """
    Dependency provider for ChatService.
    Returns a new instance of ChatService for each request.
    """
    return ChatService()

# Annotated type for easier injection
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
