import streamlit as st
import json
import os
from uuid import uuid4
import sys
import time
import threading

from runner_agent import run_agent_from_file
from utils.agent_runner import AgentController
from utils.log_buffer import StreamlitLogger
from auth.twitter_auth import get_auth_url
import uuid
from auth.twitter_auth import get_auth_url


CONFIG_DIR = "configs"
LOG_UPDATE_INTERVAL = 1  # saniye

# Sayfa ayarları
st.set_page_config(page_title="Twitter AI Agent Studio", layout="centered")
st.title("🤖 Twitter AI Agent Studio")

# Session state üzerinden Controller ve Logger'ı al
if "controller" not in st.session_state:
    st.session_state.controller = AgentController()

if "logger" not in st.session_state:
    st.session_state.logger = StreamlitLogger()

controller = st.session_state.controller
logger = st.session_state.logger

# --------------------- AGENT OLUŞTUR ---------------------
st.header("➕ Yeni Agent Oluştur")

with st.form("agent_form"):
    name = st.text_input("Agent İsmi", value=f"agent_{str(uuid4())[:5]}")
    tone = st.selectbox("Tweet Tonu", ["calm", "motivational", "funny", "professional"])
    topic = st.text_input("Tweet Konusu", "mindfulness")
    style = st.selectbox("Tweet Stili", ["formal", "casual", "informative", "engaging"])

    st.markdown("### Görevler")
    tweet_task = st.checkbox("Tweet Görevi Ekle", value=True)
    reply_task = st.checkbox("Reply Görevi Ekle", value=True)
    keywords = []

    if reply_task:
        keywords = st.text_input("Anahtar Kelimeler (Virgülle Ayırın)", "meditation, mindfulness, zen").split(",")

    submitted = st.form_submit_button("✅ Agent Oluştur")

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

        os.makedirs(CONFIG_DIR, exist_ok=True)
        config_path = os.path.join(CONFIG_DIR, f"{name}.json")
        with open(config_path, "w") as f:
            json.dump(agent_config, f)

        st.success(f"✅ Agent oluşturuldu: {name}")
        with st.expander("📄 Agent Konfigürasyonu"):
            st.code(json.dumps(agent_config, indent=2))

st.markdown("### 🔑 Twitter Hesabını Bağla")

if "oauth_session" not in st.session_state:
    st.session_state["oauth_session"] = str(uuid.uuid4())[:8]

if st.button("🔗 Twitter ile Giriş Yap"):
    url = get_auth_url(st.session_state["oauth_session"])
    if url:
        callback_info = f"http://127.0.0.1:5000/callback?state={st.session_state['oauth_session']}"
        st.success("Twitter yetkilendirme bağlantısı oluşturuldu.")
        st.markdown(f"[👉 Twitter'a Git ve Yetki Ver]({url})")
        st.markdown("Sonrasında açılan sayfada access token bilgilerini kopyalayabilirsiniz.")
    else:
        st.error("Yetkilendirme bağlantısı alınamadı.")

# --------------------- AGENT ÇALIŞTIR ---------------------
st.markdown("---")
st.header("🚀 Agent'ı Başlat / Durdur")

configs = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".json")]

if configs:
    selected_config = st.selectbox("Agent Seç:", configs)
    name = selected_config.replace(".json", "")
    path = os.path.join(CONFIG_DIR, selected_config)

    col1, col2 = st.columns(2)

    with col1:
        if controller.is_running(name):
            if st.button("🛑 Agent'ı Durdur"):
                controller.stop_agent(name)
                st.warning(f"🛑 {name} agent durduruldu.")
        else:
            if st.button("▶️ Agent'ı Başlat"):
                sys.stdout = logger  # stdout'u log'a yönlendir

                def run():
                    run_agent_from_file(path)

                thread = threading.Thread(target=run, daemon=True)
                thread.start()
                controller.start_agent(name, path)
                st.success(f"✅ {name} agent başlatıldı.")

    with col2:
        st.markdown("### ⏱ Durum")
        status = "🟢 Çalışıyor" if controller.is_running(name) else "🔴 Durmuyor"
        st.write(status)

    st.markdown("### 📜 Loglar")
    log_placeholder = st.empty()

    if controller.is_running(name):
        for _ in range(100):  # canlı log takibi
            logs = logger.get_value()
            log_placeholder.code(logs, language="text")
            time.sleep(LOG_UPDATE_INTERVAL)
else:
    st.warning("Henüz agent oluşturulmadı.")

st.markdown("---")
st.header("📦 Token'ı Agent Config Dosyasına Kaydet")

token = st.text_input("Access Token")
secret = st.text_input("Access Secret")

existing_agents = [f for f in os.listdir(CONFIG_DIR) if f.endswith(".yaml")]

if existing_agents:
    selected_agent = st.selectbox("Hangi agent config dosyasına kaydedilsin?", existing_agents)

    if st.button("💾 Token'ı Kaydet"):
        config_path = os.path.join(CONFIG_DIR, selected_agent)

        with open(config_path, "r") as f:
            config = json.safe_load(f)

        config["twitter_credentials"] = {
            "access_token": token,
            "access_secret": secret
        }

        with open(config_path, "w") as f:
            json.dump(config, f)

        st.success(f"Token bilgileri `{selected_agent}` dosyasına eklendi.")
else:
    st.warning("Hiç agent config dosyası bulunamadı.")
