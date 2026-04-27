from typing import TypedDict, List, Optional, Any, Dict


class State(TypedDict):

    conversation_id: str
    message: List[Dict[str, str]]
    current_action: Optional[str]
    search_params: Dict[str, Any]
    selected_listing_id: Optional[int]
    booking_data: Dict[str, Any]
