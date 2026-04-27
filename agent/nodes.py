import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from agent.state import State
from agent.tools import search_available_properties, get_listing_details, create_booking

load_dotenv()
# Define the tools for the agent
tools = [search_available_properties, get_listing_details, create_booking]
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    streaming=True,
    reasoning_effort="medium",
    api_key=os.environ.get("GROQ_API_KEY"),
)
assistant_runnable = llm.bind_tools(tools)


def assistant(state: State):
    """
    Interpretation node: Analyzes user input and decides on tool calls or response.
    Updates the state with the assistant's response/tool calls.
    """
    system_prompt = SystemMessage(
        content=(
            "You are StayEase AI, a helpful rental assistant for Bangladesh. "
            "You can search properties, give details, and make bookings. "
            "If a user asks for anything else, say you can't help and escalate to a human."
        )
    )
    response = assistant_runnable.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


def escalate(state: State):
    """
    Escalation node: Sets the escalation flag and notifies the user.
    """
    return {
        "escalate": True,
        "messages": [
            (
                "assistant",
                "I'm sorry, I can only help with searching, details, and bookings. I am escalating your request to a human agent.",
            )
        ],
    }
