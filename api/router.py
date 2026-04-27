from fastapi import APIRouter
from api.v1.chat import router as chat_router

router = APIRouter()

router.include_router(chat_router, prefix="/api/chat", tags=["chat"])
