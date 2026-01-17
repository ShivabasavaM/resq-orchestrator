# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph.workflow import app_graph
from app.core.state import AgentState
import uuid

app = FastAPI(title="ResQ Orchestrator", version="1.0")

# --- DATA MODELS FOR API REQUESTS ---
class ReportRequest(BaseModel):
    text: str
    thread_id: str = str(uuid.uuid4()) # Unique ID for this conversation

class ApprovalRequest(BaseModel):
    thread_id: str
    action: str = "approve" # approve / reject

# --- ENDPOINT 1: SUBMIT INCIDENT ---
@app.post("/report")
async def report_incident(req: ReportRequest):
    """
    Starts the graph. logic runs until it hits a breakpoint or finishes.
    """
    # 1. Configuration for the graph (The Thread ID is the key to memory)
    config = {"configurable": {"thread_id": req.thread_id}}
    
    # 2. Initial State
    initial_state = {
        "user_input": req.text,
        "messages": []
    }
    
    # 3. Run the graph!
    # We use invoke() but because we have a checkpointer, it pauses at interruptions
    # 3. Run the graph!
    # We add 'interrupt_after' to force a pause if we hit the review node
    events = app_graph.invoke(
        initial_state, 
        config=config, 
        interrupt_after=["human_review"] # <--- THE MAGIC BRAKE PEDAL
    )
    
    # 4. Check status
    # If the graph stopped at 'human_review', we tell the frontend to show a button
    # LangGraph snapshotting is how we peek into the current status
    snapshot = app_graph.get_state(config)
    
    status = "completed"
    if snapshot.next :
        status = "waiting_for_approval"
        
    return {
        "thread_id": req.thread_id,
        "status": status,
        "messages": events.get("messages", []),
        "incident": events.get("incident_data")
    }

# --- ENDPOINT 2: HUMAN APPROVAL ---
@app.post("/approve")
async def approve_action(req: ApprovalRequest):
    """
    Resumes the graph from the 'human_review' state.
    """
    config = {"configurable": {"thread_id": req.thread_id}}
    
    # Resume! We send a 'None' update just to nudge it forward
    # The graph knows it was paused at 'human_review', so it moves to the next edge ('dispatch')
    events = app_graph.invoke(None, config=config)
    
    return {
        "status": "resolved",
        "messages": events.get("messages", [])
    }

# --- HEALTH CHECK ---
@app.get("/")
def home():
    return {"message": "ResQ AI System Online 🟢"}