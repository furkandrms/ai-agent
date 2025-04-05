from tasks.base_task import BaseTask
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from utils.twitter_api import post_tweet

import os 
from dotenv import load_dotenv

load_dotenv()

class TweetTask(BaseTask):

    def execute(self, personality, config=None):
        
        prompt_template = PromptTemplate.from_template(
            "Write a {style}, {tone} tweet about {topic}. Keep it under 280 characters. Be authentic and engaging."
            )
        
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.7)
        chain = prompt_template | llm

        tweet = chain.invoke({

            "style": personality["style"],
            "tone": personality["tone"],
            "topic": personality["topic"]
        }).content

        print(f"[TWEET] Generated Tweet: \n{tweet}\n")
        if config and "twitter_credentials" in config:
            post_tweet(tweet, config["twitter_credentials"])
            print("[TWEET] Tweet posted successfully.")
        else:
            print(f"[ERROR] Twitter credentials not found: {config}")
            print("[WARNING] No Twitter credentials found. Tweet not posted.")

