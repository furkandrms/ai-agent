from agent import Agent 
from config_loader import load_agent_config
from tasks.tweet_task import TweetTask
from tasks.reply_task import ReplyTask
from tasks.engagement_task import EngagementTask

import os 
from dotenv import load_dotenv

from scheduler import start_scheduler

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in .env file")
else: 
    print("[INFO] OpenAI API Key found")

def task_factory(task_config): 
    if task_config["type"] == "tweet": 
        return TweetTask(task_config)
    elif task_config["type"] == "reply": 
        return ReplyTask(task_config)
    elif task_config["type"] == "engagement":
        return EngagementTask(task_config)
    else: 
        raise ValueError("Invalid task type")

def create_agent_from_config(config):
    tasks = [task_factory(t) for t in config["tasks"]]
    return Agent(config["name"], config["personality"], tasks)


def run_agent_from_file(path): 
    config = load_agent_config(path)
    agent = create_agent_from_config(config)
    agent.run(config)
    start_scheduler(agent, config)

if __name__ == "__main__": 
    config = load_agent_config("configs/zen_bot.json")
    agent = create_agent_from_config(config)
    agent.run(config)
    start_scheduler(agent, config)