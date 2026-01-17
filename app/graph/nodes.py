# app/graph/nodes.py
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.core.state import AgentState, IncidentDetails
from langchain_core.prompts import ChatPromptTemplate

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model=settings.MODEL_NAME,
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0
)

# --- NODE 1: TRIAGE (The Brain) ---
def triage_node(state: AgentState):
    print("--- TRIAGE AGENT STARTED ---")
    user_msg = state["user_input"]
    
    # Force Structured Output
    structured_llm = llm.with_structured_output(IncidentDetails)
    
    system_prompt = """You are an Emergency Coordinator. 
    Extract details. If the situation is life-threatening (fire, flood, injury), mark priority as 'High'."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    chain = prompt | structured_llm
    result = chain.invoke({"input": user_msg})
    
    return {
        "incident_data": result,
        "messages": [f"Triage: Classified as {result.priority} priority."]
    }

# --- NODE 2: HUMAN REVIEW (The Breakpoint) ---
def human_review_node(state: AgentState):
    """
    The graph will PAUSE here. 
    In the final app, this allows the UI to show an 'Approve' button.
    """
    print("--- 🛑 WAITING FOR HUMAN APPROVAL 🛑 ---")
    pass 

# --- NODE 3: DISPATCH (The Doer) ---
def dispatch_node(state: AgentState):
    print("--- 🚀 DISPATCHING RESOURCES ---")
    incident = state["incident_data"]
    
    # Simulation of an API call to dispatch units
    dispatch_log = f"DISPATCHED: {incident.required_resources} to {incident.location}"
    
    return {
        "is_resolved": True,
        "messages": [dispatch_log]
    }