# 🚑 ResQ Orchestrator: Autonomous Emergency Response System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![AI](https://img.shields.io/badge/AI-Agentic%20Workflow-purple)
![Status](https://img.shields.io/badge/Status-Deployed-green)

> **A "Human-in-the-Loop" Multi-Agent System that autonomously triages, validates, and dispatches emergency resources using LangGraph and Gemini 2.0.**

---

## 📖 About The Project

Standard LLM chatbots are often unreliable for critical operations—they hallucinate and lack "brakes." **ResQ Orchestrator** solves this by treating Emergency Response as a **State Machine**, not just a conversation.

It uses a **Graph-based Architecture** to:
1.  **Analyze** distress signals in real-time.
2.  **Make Decisions** based on severity (Low vs. High priority).
3.  **Pause Execution** for human authorization when the stakes are high.
4.  **Persist State** so the system "remembers" context even if servers restart.

### 🏗️ Architecture
This system follows a microservices pattern, decoupling the **Cognitive Engine (Backend)** from the **User Interface (Frontend)**.

```mermaid
graph TD
    User(User Report) --> API[FastAPI Gateway]
    API --> Graph[LangGraph Orchestrator]
    
    subgraph "The Brain (Agentic Graph)"
        Triage[👮 Triage Agent]
        Check{Priority High?}
        Human[🛑 Human Review Node]
        Dispatch[🚀 Dispatch Agent]
        
        Triage --> Check
        Check -- No --> Dispatch
        Check -- Yes --> Human
        Human --> Dispatch
    end
    
    Dispatch --> DB[(State Memory)]
    Human --> UI[Streamlit Dashboard]
