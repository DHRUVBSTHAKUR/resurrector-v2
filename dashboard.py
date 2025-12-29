import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURATION ---
st.set_page_config(page_title="Resurrector V2 | AI Ops", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stTextArea textarea { font-family: 'Courier New', Courier, monospace; font-size: 14px; background-color: #0d1117; color: #c9d1d9; }
    </style>
    """, unsafe_allow_html=True)

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="datarefresh")

st.title("🚀 Resurrector V2: Autonomous Control")
st.caption("Live monitoring of Phase 10 Observability and Phase 7 Repository Mapping")
st.markdown("---")

# --- SIDEBAR: TELEMETRY ---
st.sidebar.header("📊 Live Metrics")
log_dir = "logs"

if os.path.exists(log_dir):
    m_files = sorted([f for f in os.listdir(log_dir) if f.startswith("metrics_")], reverse=True)
    if m_files:
        try:
            with open(os.path.join(log_dir, m_files[0]), "r") as f:
                data = json.load(f)
                st.sidebar.metric("Run Duration", f"{data['duration_seconds']}s")
                st.sidebar.metric("Total Tokens", data['usage']['total_tokens'])
                st.sidebar.metric("Estimated Cost", data['estimated_cost_usd'])
        except Exception as e:
            st.sidebar.error(f"Error loading metrics: {e}")
    else:
        st.sidebar.info("No metrics JSON found.")

# --- MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Reasoning Trace")
    if os.path.exists(log_dir):
        log_files = sorted([f for f in os.listdir(log_dir) if f.startswith("resurrector_log")], reverse=True)
        if log_files:
            selected_log = st.selectbox("Select History Session", log_files)
            with open(os.path.join(log_dir, selected_log), "r") as f:
                st.text_area("Live Terminal Feed", f.read(), height=600)

with col2:
    st.subheader("🌿 Workspace Files")
    workspace = "agent_workspace"
    if os.path.exists(workspace):
        all_files = [{"File": os.path.relpath(os.path.join(root, f), workspace)} 
                     for root, _, filenames in os.walk(workspace) for f in filenames]
        if all_files:
            # ✅ FIXED: width="stretch" satisfies the Streamlit validator
            st.dataframe(pd.DataFrame(all_files), width="stretch", hide_index=True)
    
    st.markdown("---")
    st.subheader("🛡️ Security Review Status")
    if 'selected_log' in locals():
        with open(os.path.join(log_dir, selected_log), "r") as f:
            content = f.read().upper()
            if "APPROVE" in content: st.success("LATEST STATUS: APPROVED")
            elif "REJECT" in content: st.error("LATEST STATUS: REJECTED")
            else: st.warning("LATEST STATUS: PENDING")