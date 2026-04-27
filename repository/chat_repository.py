import json
from typing import List, Any
from langchain_core.messages import messages_from_dict, messages_to_dict
from db.db import get_db_connection

class ChatRepository:
    """
    Repository for handling conversation persistence in the database.
    Separates database SQL logic from business logic.
    """

    def load_history(self, conversation_id: str) -> List[Any]:
        """Retrieve conversation history from the database and deserialize it."""
        query = "SELECT history FROM conversations WHERE id = %s"
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (conversation_id,))
                result = cur.fetchone()
                if result and result[0]:
                    return messages_from_dict(result[0])
        return []

    def save_history(self, conversation_id: str, messages: List[Any]):
        """Serialize and persist the conversation history to the database."""

        history_json = messages_to_dict(messages)
        
        query = """
        INSERT INTO conversations (id, history)
        VALUES (%s, %s)
        ON CONFLICT (id) DO UPDATE SET history = EXCLUDED.history;
        """
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (conversation_id, json.dumps(history_json)))
                conn.commit()
