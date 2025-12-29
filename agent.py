import os
import json
from typing import TypedDict, List, Annotated
from dotenv import load_dotenv

# --- 0. SOTA OBSERVABILITY ---
import phoenix as px
from phoenix.otel import register

# 1. Launch Dashboard
session = px.launch_app()

# 2. Connect Pipe
register(
    project_name="default",
    endpoint="http://localhost:6006/v1/traces",
    auto_instrument=True
)
print(f"🕵️  Trace Server Live at: {session.url}")

# --- IMPORTS ---
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage, BaseMessage, ToolMessage, AIMessage, SystemMessage
)
from twilio.rest import Client

# Custom Modules
from sandbox import Sandbox
from observability import ResurrectorTracker

# --- 1. INITIALIZE ---
load_dotenv()
tracker = ResurrectorTracker()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_retries=2,
)

# --- 2. DEFINE STATE ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    review_status: str

# --- 3. DEFINE TOOLS ---
def run_command(command: str):
    sandbox = Sandbox()
    return sandbox.run_command(command)

def edit_file(file_path: str, content: str):
    sandbox = Sandbox()
    return sandbox.edit_file(file_path, content)

def read_file(file_path: str):
    sandbox = Sandbox()
    return sandbox.read_file(file_path)

tools = [run_command, edit_file, read_file]
llm_with_tools = llm.bind_tools(tools)

# --- 4. DEFINE NODES ---

def reason_node(state: AgentState):
    """The Junior Developer."""
    print("\n🧠 Junior Dev: Thinking...")
    try:
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    except Exception as e:
        print(f"❌ LLM ERROR: {e}")
        return {"messages": [AIMessage(content="Error processing. Retrying.")]}

def action_node(state: AgentState):
    """The Hands."""
    last_message = state["messages"][-1]
    tool_results = []
    
    if not last_message.tool_calls:
        return {"messages": []}

    for tool_call in last_message.tool_calls:
        print(f"🛠️  Tool Call: {tool_call['name']}")
        try:
            if tool_call['name'] == "run_command":
                res = run_command(**tool_call['args'])
            elif tool_call['name'] == "edit_file":
                res = edit_file(**tool_call['args'])
            elif tool_call['name'] == "read_file":
                res = read_file(**tool_call['args'])
            else:
                res = "Error: Unknown tool."
        except Exception as e:
            res = f"Tool Execution Error: {str(e)}"
        
        tool_results.append(ToolMessage(
            tool_call_id=tool_call['id'],
            name=tool_call['name'],
            content=str(res)
        ))
    return {"messages": tool_results}

def review_node(state: AgentState):
    """The Critic (Principal Security Engineer)."""
    print("\n🛡️  Principal Security Engineer: Reviewing PR...")
    
    critic_prompt = """
    You are a Principal Security Engineer reviewing a Junior Developer's fix.
    
    CRITERIA FOR APPROVAL:
    1. Did the Junior Dev run the code and confirm it works?
    2. Does the code look safe (no rm -rf, no infinite loops)?
    
    If YES to both, respond "APPROVE".
    If NO, respond "REJECT" and explain why.
    
    NOTE: If the Junior Dev says "I fixed it" and ran the script successfully, just APPROVE it. Don't be too strict.
    """
    
    messages = state["messages"] + [HumanMessage(content=critic_prompt)]
    response = llm.invoke(messages)
    content = response.content.strip()
    
    status = "approved" if "APPROVE" in content.upper() else "rejected"
    print(f"⚖️  Verdict: {status.upper()}")
    
    if status == "rejected":
        return {
            "review_status": "rejected",
            "messages": [HumanMessage(content=f"Security Review Failed: {content}. Please verify the fix by running the script.")]
        }
    
    return {"review_status": "approved"}

# --- 5. NOTIFICATION SYSTEM ---
def notify_success():
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    to_num = os.getenv("TWILIO_TO_NUMBER")
    from_num = os.getenv("TWILIO_FROM_NUMBER")
    
    if not (sid and token and to_num and from_num):
        # Silent pass if no keys
        return

    try:
        client = Client(sid, token)
        client.calls.create(
            twiml='<Response><Say>Resurrector Alert. Pipeline fixed.</Say></Response>',
            to=to_num,
            from_=from_num
        )
    except Exception:
        pass

# --- 6. GRAPH SETUP ---
workflow = StateGraph(AgentState)
workflow.add_node("reason", reason_node)
workflow.add_node("act", action_node)
workflow.add_node("review", review_node)

workflow.set_entry_point("reason")

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "act"
    return "review"

def review_gate(state: AgentState):
    if state["review_status"] == "rejected":
        print("🔄 Loops back to Junior Dev...")
        return "reason"
    return END

workflow.add_conditional_edges("reason", should_continue, {"act": "act", "review": "review"})
workflow.add_edge("act", "reason")
workflow.add_conditional_edges("review", review_gate, {"reason": "reason", END: END})

app = workflow.compile()

# --- 7. RUN ---
def start_resurrection():
    print("🚀 Starting Multi-Agent Security Run...")
    initial_state = {
        "messages": [
            SystemMessage(content="You are a Junior DevOps Engineer. Fix the code. IMPORTANT: You must RUN the python script to verify your fix works before submitting."),
            HumanMessage(content="The pipeline failed. Fix the Python script error.")
        ],
        "review_status": "pending"
    }
    
    # Increased recursion limit to prevent crashes during long debug loops
    app.invoke(initial_state, config={"recursion_limit": 50})
    
    print("\n✅ AGENT RUN COMPLETE")
    notify_success()

if __name__ == "__main__":
    start_resurrection()
    input("\n👀 Trace server is active. Press Enter to exit...")