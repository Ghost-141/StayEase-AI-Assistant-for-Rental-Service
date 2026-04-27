from typing import List, Dict, Any
from langchain_core.messages import HumanMessage
from agent.graph import graph
from repository.chat_repository import ChatRepository
from core.logger import setup_logger

logger = setup_logger(__name__)

class ChatService:
    """
    Orchestration service for handling AI chat interactions.
    Now uses the ChatRepository for data persistence.
    """
    
    def __init__(self):
        # Initialize the repository
        self.repository = ChatRepository()
    
    def process_message(self, conversation_id: str, user_message: str) -> Dict[str, Any]:
        """
        Process a user message through the agentic graph and persist state.
        """
        logger.info(f"Processing message for conversation {conversation_id}...")
        # Load history via repository
        history = self.repository.load_history(conversation_id)
        
        inputs = {
            "messages": history + [HumanMessage(content=user_message)],
            "escalate": False
        }
        
        # Run agent logic
        final_state = graph.invoke(inputs)
        
        # Persist state via repository
        self.repository.save_history(conversation_id, final_state["messages"])
        
        last_message = final_state["messages"][-1]
        logger.info(f"Successfully processed message for conversation {conversation_id}.")
        
        return {
            "response": last_message.content,
            "escalated": final_state.get("escalate", False)
        }

    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Retrieve and format the history for a specific conversation.
        """
        # Load messages via repository
        messages = self.repository.load_history(conversation_id)
        
        return [
            {"role": "user" if m.type == "human" else "assistant", "content": m.content}
            for m in messages if hasattr(m, "content") and m.content
        ]

# Export an instance (though the DI layer now creates fresh ones)
chat_service = ChatService()
