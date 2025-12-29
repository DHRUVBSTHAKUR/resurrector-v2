import time
import json
import os

class ResurrectorTracker:
    def __init__(self):
        self.start_time = time.time()
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        
        # Current Gemini 2.0 Flash Pricing (Approximate per 1M tokens)
        self.COST_PER_1K_INPUT = 0.0001  # $0.10 per 1M
        self.COST_PER_1K_OUTPUT = 0.0004 # $0.40 per 1M

    def track_usage(self, response):
        """
        Scans the AI response for token usage across different metadata schemas.
        """
        try:
            # 1. Primary: Check for standard usage_metadata
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                self.total_input_tokens += response.usage_metadata.get('input_tokens', 0)
                self.total_output_tokens += response.usage_metadata.get('output_tokens', 0)
                return

            # 2. Fallback: Check response_metadata (common in older LangChain-Google versions)
            if hasattr(response, 'response_metadata'):
                meta = response.response_metadata
                usage = meta.get('usage') or meta.get('token_usage')
                if usage:
                    self.total_input_tokens += usage.get('prompt_tokens', 0)
                    self.total_output_tokens += usage.get('completion_tokens', 0)

        except Exception as e:
            print(f"⚠️ Telemetry Error: Could not parse tokens - {e}")

    def get_report(self):
        """Calculates duration, total tokens, and USD cost."""
        duration = time.time() - self.start_time
        
        input_cost = (self.total_input_tokens / 1000) * self.COST_PER_1K_INPUT
        output_cost = (self.total_output_tokens / 1000) * self.COST_PER_1K_OUTPUT
        total_cost = input_cost + output_cost
        
        return {
            "status": "COMPLETED",
            "duration_seconds": round(duration, 2),
            "usage": {
                "input_tokens": self.total_input_tokens,
                "output_tokens": self.total_output_tokens,
                "total_tokens": self.total_input_tokens + self.total_output_tokens
            },
            "estimated_cost_usd": f"${total_cost:.6f}"
        }

    def save_report(self, log_dir="logs"):
        """
        Saves the metrics to a JSON file. 
        The Dashboard reads the latest file to display metrics in the sidebar.
        """
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        report = self.get_report()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(log_dir, f"metrics_{timestamp}.json")
        
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)
        
        return report_path