from agent import Agent 
from config_loader import load_agent_config
from tasks.tweet_task import TweetTask
from tasks.reply_task import ReplyTask

import os 
from dotenv import load_dotenv

load_dotenv()

def task_factory(task_config): 
    if task_config["type"] == "tweet": 
        return TweetTask(task_config)
    elif task_config["type"] == "reply": 
        return ReplyTask(task_config)
    else: 
        raise ValueError("Invalid task type")

def create_agent_from_config(config): 
    tasks = [task_factory(t) for t in config["tasks"]]
    return Agent(config["name"], config["personality"], tasks)

if __name__ == "__main__": 
    config = load_agent_config("configs/zen_bot.json")
    agent = create_agent_from_config(config)
    agent.run()