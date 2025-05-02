import streamlit as st
import json
import os
import uuid
import sys
import time
import threading

from runner_agent import run_agent_from_file
from utils.agent_runner import AgentController
from utils.log_buffer import StreamlitLogger
from auth.twitter_auth import get_auth_url

CONFIG_DIR = "configs"
LOG_UPDATE_INTERVAL = 1  # seconds

# Page settings
st.set_page_config(page_title="Twitter AI Agent Studio", layout="centered")
st.title("🤖 Twitter AI Agent Studio")

# Session state controller and logger
if "controller" not in st.session_state:
    st.session_state.controller = AgentController()

if "logger" not in st.session_state:
    st.session_state.logger = StreamlitLogger()

controller = st.session_state.controller
logger = st.session_state.logger

# --------------------- CREATE AGENT ---------------------
st.header("➕ Create New Agent")

with st.form("agent_form"):
    name = st.text_input("Agent Name", value=f"agent_{str(uuid.uuid4())[:5]}")
    tone = st.selectbox("Tweet Tone", ["calm", "motivational", "funny", "professional"])
    topic = st.text_input("Tweet Topic", "mindfulness")
    style = st.selectbox("Tweet Style", ["formal", "casual", "informative", "engaging"])

    st.markdown("### Tasks")
    tweet_task = st.checkbox("Add Tweet Task", value=True)
    reply_task = st.checkbox("Add Reply Task", value=True)
    engagement_task = st.checkbox("Add Engagement Task", value=True)
    engagement_actions = []
    engagement_keywords = []
    keywords = []

    if engagement_task:
        engagement_actions = st.multiselect(
            "Engagement Actions",
            ["like", "retweet", "follow"],
            default=["like"]
        )
        engagement_keywords = st.text_input(
            "Engagement Keywords (comma-separated)",
            "meditation, mindfulness, zen"
        ).split(",")

    if reply_task:
        keywords = st.text_input("Keywords (comma-separated)", "meditation, mindfulness, zen").split(",")

    submitted = st.form_submit_button("✅ Create Agent")

if submitted:
    agent_config = {
        "name": name,
        "personality": {
            "tone": tone,
            "topic": topic,
            "style": style
        },
        "tasks": []
    }

    if tweet_task:
        agent_config["tasks"].append({
            "type": "tweet",
            "frequency": "daily"
        })
    if reply_task:
        agent_config["tasks"].append({
            "type": "reply",
            "frequency": "daily",
            "keywords": [kw.strip() for kw in keywords]
        })
    
    if engagement_task:
        agent_config["tasks"].append({
            "type": "engagement",
            "frequency": "daily",
            "keywords": [kw.strip() for kw in keywords],
            "actions": engagement_actions
        })

    os.makedirs(CONFIG_DIR, exist_ok=True)
    config_path = os.path.join(CONFIG_DIR, f"{name}.json")
    with open(config_path, "w") as f:
        json.dump(agent_config, f)

    st.success(f"✅ Agent created: {name}")
    with st.expander("📄 Agent Configuration"):
        st.code(json.dumps(agent_config, indent=2))

    # Save to session
    st.session_state["last_created_agent"] = name
    st.session_state["oauth_session"] = str(uuid.uuid4())[:8]

    # Twitter auth link
    st.markdown("### 🔑 Connect Twitter Account")
    config_filename = os.path.join(CONFIG_DIR, f"{name}.json")
    url = get_auth_url(config_path)
    if url:
        st.success("Twitter authorization link created.")
        st.markdown(f"[👉 Go to Twitter and Authorize]({url})")
        st.markdown("After authorization, access token will be automatically saved for this agent.")
    else:
        st.error("Failed to generate authorization link.")

# --------------------- RUN / STOP AGENT ---------------------
st.markdown("---")
st.header("🚀 Start / Stop Agent")

configs = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".json")]

if configs:
    selected_config = st.selectbox("Select Agent:", configs)
    name = selected_config.replace(".json", "")
    path = os.path.join(CONFIG_DIR, selected_config)

    col1, col2 = st.columns(2)

    with col1:
        if controller.is_running(name):
            if st.button("🛑 Stop Agent"):
                controller.stop_agent(name)
                st.warning(f"🛑 Agent {name} has been stopped.")
        else:
            if st.button("▶️ Start Agent"):
                sys.stdout = logger  # Redirect stdout to logger

                def run():
                    run_agent_from_file(path)

                thread = threading.Thread(target=run, daemon=True)
                thread.start()
                controller.start_agent(name, path)
                st.success(f"✅ Agent {name} has started.")

    with col2:
        st.markdown("### ⏱ Status")
        status = "🟢 Running" if controller.is_running(name) else "🔴 Stopped"
        st.write(status)

    st.markdown("### 📜 Logs")
    log_placeholder = st.empty()

    if controller.is_running(name):
        for _ in range(100):  # live log tracking
            logs = logger.get_value()
            log_placeholder.code(logs, language="text")
            time.sleep(LOG_UPDATE_INTERVAL)
else:
    st.warning("No agent has been created yet.")
