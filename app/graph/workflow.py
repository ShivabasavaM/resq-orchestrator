from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver # <--- This enables the "Pause & Resume" feature
from app.core.state import AgentState
from app.graph.nodes import triage_node, human_review_node, dispatch_node

# --- 1. CONDITIONAL LOGIC ---
def route_incident(state: AgentState):
    """
    Decides where to go next based on priority.
    """
    # We access the structured data stored in the state
    incident = state.get("incident_data")
    
    # Safety check: if for some reason incident data is missing, we default to dispatch
    if not incident:
        return "dispatch"
    
    # The Logic: High Priority triggers the human review pause
    if incident.priority == "High":
        return "human_review" 
    else:
        return "dispatch" 

# --- 2. BUILD THE GRAPH ---
workflow = StateGraph(AgentState)

# Add Nodes (The Workers)
workflow.add_node("triage", triage_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("dispatch", dispatch_node)

# Add Edges (The Connections)
workflow.set_entry_point("triage")

# Add Conditional Edge (The Decision Point)
# From "triage", we use the "route_incident" function to decide where to go
workflow.add_conditional_edges(
    "triage",
    route_incident,
    {
        "human_review": "human_review",
        "dispatch": "dispatch"
    }
)

# Add Standard Edges
# After human review is done (resumed), we always go to dispatch
workflow.add_edge("human_review", "dispatch")
# After dispatch, the job is done
workflow.add_edge("dispatch", END)

# --- 3. COMPILE WITH MEMORY ---
# We initialize the memory saver. This stores the state in RAM.
# In a production app, you would swap this for a PostgresSaver (database).
checkpointer = MemorySaver()

# We pass the checkpointer to compile() so the graph can "remember" and pause.
app_graph = workflow.compile(checkpointer=checkpointer)