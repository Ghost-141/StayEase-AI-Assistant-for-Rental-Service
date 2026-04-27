from typing import Annotated, TypedDict, Optional, Dict, Any
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
    The state of the StayEase AI agent.

    Attributes:
        messages: The conversation history, updated using the add_messages reducer.
        search_params: Extracted search criteria like location, dates, and guests.
        selected_listing: Details of a property the user is currently interested in.
        escalate: Boolean flag to indicate if the request should be handled by a human.
    """

    messages: Annotated[list, add_messages]
    search_params: Optional[Dict[str, Any]]
    selected_listing: Optional[Dict[str, Any]]
    escalate: bool
