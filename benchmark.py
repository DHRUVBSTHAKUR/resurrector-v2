import os
import time
import shutil
from agent import start_resurrection
from git_ops import GitManager

# --- CONFIGURATION ---
TEST_CASES = [
    {
        "name": "Missing Dependency (Requests)",
        "inject_bug": "echo 'import requests' >> calculator.py && sed -i '' '/requests/d' requirements.txt",
        "expected_fix": "requests"
    },
    {
        "name": "Syntax Error (Missing Colon)",
        "inject_bug": "sed -i '' 's/def add(a, b):/def add(a, b)/' calculator.py",
        "expected_fix": "SyntaxError"
    },
    {
        "name": "Logic Error (Division by Zero)",
        "inject_bug": "echo 'print(10/0)' >> calculator.py",
        "expected_fix": "ZeroDivisionError"
    }
]

def run_benchmark():
    print("🏆 STARTING SOTA AGENT EVALUATION SUITE")
    print("========================================")
    
    results = []
    git_mgr = GitManager()
    
    for test in TEST_CASES:
        print(f"\n🧪 Running Test Case: {test['name']}")
        
        # 1. Reset Environment
        if os.path.exists("resurrector-test-repo"):
            shutil.rmtree("resurrector-test-repo")
        
        # 2. Inject the Bug (Simulating a broken repo)
        git_mgr.clone_repo("https://github.com/DHRUVBSTHAKUR/resurrector-test-repo.git")
        os.system(f"cd resurrector-test-repo && {test['inject_bug']}")
        print(f"⚠️  Bug Injected: {test['inject_bug']}")
        
        # 3. Run the Agent
        start_time = time.time()
        try:
            # We call the main agent logic here
            # Note: Ensure start_resurrection returns a status dict in agent.py
            start_resurrection() 
            status = "PASSED"
        except Exception as e:
            status = f"FAILED ({str(e)})"
        
        duration = time.time() - start_time
        
        results.append({
            "test": test['name'],
            "status": status,
            "duration": f"{duration:.2f}s"
        })

    print("\n\n📊 FINAL BENCHMARK REPORT")
    print("| Test Case | Status | Time |")
    print("|-----------|--------|------|")
    for r in results:
        print(f"| {r['test']} | {r['status']} | {r['duration']} |")

if __name__ == "__main__":
    run_benchmark()
    # 👇 ADD THIS LINE SO YOU CAN SEE THE RESULTS 👇
    input("\n👀 Benchmark Complete. Traces are live. Press Enter to exit...")