# ⚡️ Resurrector V2: The Self-Healing DevOps Engine

<div align="center">

![Status](https://img.shields.io/badge/Status-Production%20Grade-success?style=for-the-badge)
![Autonomy](https://img.shields.io/badge/Autonomy-Level%204%20(Multi--Agent)-orange?style=for-the-badge)
![Tech](https://img.shields.io/badge/Model-Gemini%202.0%20Flash-blueviolet?style=for-the-badge)
![Observability](https://img.shields.io/badge/Observability-OpenTelemetry-blue?style=for-the-badge)

**An autonomous AI workforce that hunts bugs, patches code, and audits itself—while you sleep.**

[View Traces](http://localhost:6006) • [Report Bug](https://github.com/DHRUVBSTHAKUR/resurrector-v2/issues)

---

### 🎥 Watch Level 4 Autonomy in Action
*The agent detects a `ZeroDivisionError`, attempts a fix, gets REJECTED by the Security Auditor, auto-corrects, and passes on the second try.*

![Resurrector Demo](https://github.com/DHRUVBSTHAKUR/resurrector-v2/issues/1#issue-3768218921)

</div>

---

## 🛑 The "Million Dollar" Problem
Modern CI/CD pipelines are fragile. A missing dependency, a forgotten colon, or a logic error can halt production for hours while on-call engineers scramble.
> **The Solution:** A **Multi-Agent AI System** that doesn't just "suggest" code—it spins up a secure sandbox, reproduces the crash, fixes it, and **verifies the fix** against a rigorous security audit before merging.

## 🧠 System Architecture (Level 4 Autonomy)

This isn't a simple chatbot. It is a **Self-Correcting Reasoning Loop** built on **LangGraph**.

### 🎭 The Cast
1.  **👷‍♂️ Agent A: The Junior DevOps (Execution)**
    * **Role:** The "Hands." Reads `stderr` logs, locates files, and injects fixes.
    * **Constraint:** Must provide "Proof of Work" (successful execution logs) before submitting.
    * **Engine:** `Gemini 2.0 Flash` (P50 Latency: 1.3s).

2.  **🛡️ Agent B: The Principal Security Engineer (Audit)**
    * **Role:** The "Eyes." Reviews the PR for security risks (e.g., `rm -rf`, infinite loops).
    * **Power:** Can **REJECT** the fix and force Agent A to retry.
    * **Engine:** `Gemini 2.0 Flash` (Strict Prompting).

---

## 📊 The "Gauntlet": Performance Benchmark
I subjected the system to a regression suite of 3 distinct failure modes. It achieved a **100% Success Rate** with zero human intervention.

| Failure Mode | Bug Type | Agent Behavior | Time-to-Fix | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Missing Lib** | `ImportError` | Installed dependency via `pip` | **~2.9s** | ✅ PASSED |
| **Syntax Error** | `SyntaxError` | Parsed trace, inserted colon | **~2.3s** | ✅ PASSED |
| **Logic Crash** | `ZeroDivision` | **REJECTED** 1st attempt → Refactored → **APPROVED** | **~5.4s** | ✅ PASSED |

> **📉 Cost Efficiency:** The entire regression suite runs for **<$0.01** using Gemini 2.0 Flash.

---

## 🛠️ Tech Stack & Engineering
* **Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/) (Stateful Multi-Agent Loops)
* **Sandboxing:** [Docker](https://www.docker.com/) (Ephemeral Execution Environments)
* **Intelligence:** [Google Gemini 2.0 Flash](https://deepmind.google/technologies/gemini/) (Multimodal Reasoning)
* **Observability:** [Arize Phoenix](https://phoenix.arize.com/) (OpenTelemetry Tracing)
* **Notifications:** [Twilio](https://www.twilio.com/) (Voice Alerts on Success)

## 🔬 Observability (The "X-Ray")
Every thought, tool call, and state transition is traced live via **Arize Phoenix**.

* **Green Checkmarks:** Successful reasoning steps.
* **Red Exclamations:** Failed attempts (automatically retried).
* **Latency P50:** 1.3 seconds.

---

## 🚀 How to Run

### 1. Clone & Install
```bash
git clone [https://github.com/DHRUVBSTHAKUR/resurrector-v2.git](https://github.com/DHRUVBSTHAKUR/resurrector-v2.git)
cd resurrector-v2
uv sync  # Installs dependencies fast

## 2. Configure Secrets

Create a `.env` file:

```ini
GOOGLE_API_KEY="your_gemini_key"
TWILIO_ACCOUNT_SID="optional"
TWILIO_AUTH_TOKEN="optional"


## 3. Unleash the Agents

```bash
uv run benchmark.py
```

## 🔮 Roadmap

- [x] Self-Healing Loop: Logic error rejection and retry
- [x] Secure Sandbox: Docker containerization
- [x] SOTA Speed: Migration to Gemini 2.0 Flash
- [ ] Voice Mode: Call the on-call engineer when a fix is merged (Twilio integration ready)
- [ ] GitHub Integration: Auto-open PRs on repository issues