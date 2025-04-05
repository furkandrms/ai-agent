# 🔠 Twitter AI Agent Framework

An AI-powered, customizable, and modular Twitter bot framework.  
Users can easily create their own AI-driven "agents" to automate Twitter engagement such as tweeting, replying to mentions, and performing analysis.

## 🚀 Features

- ✅ Content generation with OpenAI (GPT-powered)
- ✅ Agent creation and launch via Streamlit interface
- ✅ LangChain-supported content generation structure
- ✅ Task scheduler (for tweeting/replying)
- ✅ Real Twitter API v2 support (Tweepy + OAuth 2.0) for tweeting and mention replying
- ✅ Custom `config.json` for each agent
- ✅ Task logging (`tweets_log.json`)

## 🗄️ Demo

![demo](/assets/create_agent.png)

---

## 📆 Installation

### 1. Clone the repo

```bash
git clone https://github.com/furkandrms/ai-agent.git
cd twitter-ai-agent
```

### 2. Install the required libraries

```bash
pip install -r requirements.txt
```

> Key dependencies include:
> - `tweepy`
> - `openai`
> - `langchain`
> - `streamlit`
> - `apscheduler`
> - `python-dotenv`

### 3. Define environment variables (`.env` file)

```env
OPENAI_API_KEY=your-openai-key
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_BEARER_TOKEN=...
```

> ⚠️ Each agent’s `access_token` is stored in its individual config.

---

## 🧠 Agent Structure

Agents are defined using JSON or YAML. Example `config`:

```json
name: zen_bot
personality:
  tone: calm
  topic: mindfulness
  style: formal
tasks:
  - type: tweet
    frequency: daily
  - type: reply
    frequency: 10min
    keywords: ["meditation", "mindfulness", "zen"]
twitter_credentials:
  access_token: "user_access_token"
  access_secret: "user_access_secret"
```

---

## 🖥️ Usage

### Launch the Streamlit interface

```bash
streamlit run streamlit_app.py
```

- Create an agent  
- Define tweet and reply tasks  
- Launch your agent  
- Watch logs in real-time

---

## 🔁 Task Types

| Task      | Description                                      |
|-----------|--------------------------------------------------|
| tweet     | Generates content with GPT and posts as a tweet  |
| reply     | Scans mentions and generates GPT-powered replies |
| (coming)  | thread, dm, analysis tasks                       |

---

## 🗂️ File Structure

```
├── agent.py
├── runner_agent.py
├── streamlit_app.py
├── tasks/
│   ├── tweet_task.py
│   └── reply_task.py
├── utils/
│   ├── twitter_api.py
│   └── log_buffer.py
├── configs/
│   └── zen_bot.json
├── tweets_log.json
├── .env
└── README.md
```

---

## ✨ Roadmap

- [ ] Thread creation feature
- [ ] Follower analysis and content optimization
- [ ] Memory & LangChain Agent integration

---

## 👨‍💼 Contributing

Feel free to open a PR or create an [issue](https://github.com/furkandrms/ai-agent/issues) if you'd like to contribute.

---

## 📄 License

MIT License

---

> **This project was inspired by [elizaOS/eliza](https://github.com/elizaOS/eliza).**
