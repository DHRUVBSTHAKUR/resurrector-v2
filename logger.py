import os
from datetime import datetime
from langchain_core.messages import AIMessage  # ✅ Added this import

class ThoughtLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"resurrector_log_{timestamp}.txt")

    def log_event(self, category, content):
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] [{category.upper()}]\n{content}\n")
            f.write("-" * 50 + "\n")

    def log_state(self, state):
        if state.get("messages"):
            last_msg = state["messages"][-1]
            # Now AIMessage is defined for this check
            role = "AI" if isinstance(last_msg, AIMessage) else "System/Tool/Human"
            self.log_event(role, getattr(last_msg, 'content', str(last_msg)))