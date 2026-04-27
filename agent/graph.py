from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from agent.state import State
from agent.nodes import assistant, escalate, tools


# Initialize the Graph
builder = StateGraph(State)

# Add Nodes
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("escalate", escalate)

# Define Edges & Routing
builder.add_edge(START, "assistant")


# Conditional routing from assistant
def route_assistant(state: State):
    # 1. Use prebuilt tools_condition to check for tool calls
    route = tools_condition(state)
    if route == "tools":
        return "tools"

    # 2. Check for escalation if no tool calls are present
    last_message = state["messages"][-1]
    content = last_message.content.lower()
    if "escalat" in content or "human" in content:
        return "escalate"

    return END


builder.add_conditional_edges(
    "assistant",
    route_assistant,
    {"tools": "tools", "escalate": "escalate", "__end__": END},
)

# After tools, always return to assistant to process results
builder.add_edge("tools", "assistant")

# After escalation, end the flow
builder.add_edge("escalate", END)

# Compile the Graph
graph = builder.compile()
