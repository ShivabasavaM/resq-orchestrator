from typing import TypedDict, Annotated, List, Optional
import operator
from pydantic import BaseModel, Field

# --- 1. Data Models (Strict structure for the LLM to fill) ---
class IncidentDetails(BaseModel):
    """Structured extraction of the emergency."""
    location: str = Field(description="The physical location of the incident")
    incident_type: str = Field(description="Type of incident: Medical, Rescue, Logistics, Other")
    priority: str = Field(description="High, Medium, or Low based on urgency")
    summary: str = Field(description="A concise 1-sentence summary of the situation")
    required_resources: List[str] = Field(description="List of assets needed, e.g., 'Ambulance', 'Boat'")

# --- 2. Graph State (The Memory) ---
class AgentState(TypedDict):
    """
    The state of the graph. This dict is passed between all nodes.
    """
    # Raw input from the user
    user_input: str
    
    # The structured incident data (Initially None until Triage runs)
    incident_data: Optional[IncidentDetails]
    
    # Conversation history (Append-only log)
    messages: Annotated[List[str], operator.add]
    
    # Flags for logic control
    is_escalated: bool
    is_resolved: bool