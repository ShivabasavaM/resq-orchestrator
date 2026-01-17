import streamlit as st
import requests
import uuid
import json
import os

# --- CONFIGURATION ---
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="ResQ Orchestrator", layout="wide")

# --- SESSION STATE (To remember data) ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_status" not in st.session_state:
    st.session_state.current_status = "idle"

# --- SIDEBAR (Controls) ---
st.sidebar.title("🚑 ResQ Command Center")
st.sidebar.markdown(f"**Session ID:** `{st.session_state.thread_id}`")
if st.sidebar.button("New Session / Clear"):
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.current_status = "idle"
    st.rerun()

# --- MAIN UI ---
st.title("🤖 Autonomous Emergency Response System")
st.markdown("---")

# 1. Input Section
col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("Incoming Distress Signal:", height=100, placeholder="E.g., Major fire at Tech Park, need evacuation...")
    
    if st.button("🚨 Report Incident", type="primary"):
        if user_input:
            with st.spinner("Agents are analyzing..."):
                payload = {"text": user_input, "thread_id": st.session_state.thread_id}
                try:
                    res = requests.post(f"{API_URL}/report", json=payload)
                    data = res.json()
                    
                    st.session_state.messages = data.get("messages", [])
                    st.session_state.current_status = data.get("status")
                    st.rerun()
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# 2. Display Status & Actions
with col2:
    st.subheader("System Status")
    if st.session_state.current_status == "waiting_for_approval":
        st.warning("⚠️ CRITICAL ACTION REQUIRED")
        st.write("The AI has paused for Human Authorization.")
        
        if st.button("✅ APPROVE DISPATCH"):
            with st.spinner("Dispatching units..."):
                payload = {"thread_id": st.session_state.thread_id, "action": "approve"}
                res = requests.post(f"{API_URL}/approve", json=payload)
                data = res.json()
                
                # Append new logs
                st.session_state.messages.extend(data.get("messages", []))
                st.session_state.current_status = "resolved"
                st.rerun()
                
    elif st.session_state.current_status == "resolved":
        st.success("✅ INCIDENT RESOLVED")
    else:
        st.info("System Standby")

# 3. Live Agent Logs
st.markdown("---")
st.subheader("📝 Live Agent Operations Log")
for msg in st.session_state.messages:
    if "TRIAGE" in msg.upper():
        st.info(f"🧠 {msg}")
    elif "DISPATCHED" in msg.upper():
        st.success(f"🚚 {msg}")
    else:
        st.write(msg)