from fastapi import APIRouter, HTTPException, status
from core.dependency import ChatServiceDep
from schemas.chat_models import ChatRequest, ChatResponse, HistoryResponse
from core.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/{conversation_id}/message", response_model=ChatResponse)
async def send_message(
    conversation_id: str, request: ChatRequest, service: ChatServiceDep
):
    """
    Endpoint to send a message to the AI agent.
    """
    try:
        logger.info(f"Received message for conversation_id: {conversation_id}")
        result = service.process_message(conversation_id, request.message)

        return ChatResponse(
            messages=[{"role": "assistant", "content": result["response"]}],
            escalated=result["escalated"],
        )

    except Exception as e:
        logger.error(
            f"Error in send_message for id: {conversation_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error. Please check server logs.",
        )


@router.get("/{conversation_id}/history", response_model=HistoryResponse)
async def get_chat_history(conversation_id: str, service: ChatServiceDep):
    """
    Endpoint to retrieve the conversation history.
    """
    try:
        logger.info(f"Retrieving history for conversation_id: {conversation_id}")
        history = service.get_conversation_history(conversation_id)

        if not history:
            logger.warning(f"No history found for conversation_id: {conversation_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation history not found.",
            )

        return HistoryResponse(conversation_id=conversation_id, history=history)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error in get_chat_history for id: {conversation_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error. Please check server logs.",
        )
