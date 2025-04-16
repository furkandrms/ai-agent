from tasks.base_task import BaseTask
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from utils.twitter_api import get_recent_mentions, reply_to_tweet

import time
from tweepy.errors import TooManyRequests

from dotenv import load_dotenv
import os

load_dotenv()

class ReplyTask(BaseTask):

    def execute(self, personality, config=None):
        credentials = config.get("twitter_credentials") if config else None

        if not credentials:
            print("[ERROR] Twitter credentials not found in config.")
            return
        keywords = self.config.get("keywords", [])
        try:
            mentions = get_recent_mentions(credentials)
        except TooManyRequests as e:
            print("[RATE LIMIT] Mention çekimi limitlendi. Daha sonra tekrar denenecek.")
            time.sleep(60)  # Wait for 1 minute before retrying
            return 
        
        for tweet in mentions: 
            text = tweet["text"]
            if any(kw.lower() in text.lower() for kw in keywords): 
                print(f"[MATCH] Keyword matched in tweet: {text}")

                prompt_template = PromptTemplate.from_template(
                    "Reply to this tweet in a {tone} and {style} way about {topic}:\n\n\"{tweet}\""
                )

                llm= ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key= os.getenv("OPENAI_API_KEY"), temperature=0.7, max_tokens=100)
                chain = prompt_template | llm

                response = chain.invoke({
                    "tone": personality["tone"],
                    "style": personality["style"],
                    "topic": personality["topic"],
                    "tweet": text
                }).content

                reply_to_tweet(tweet["id"], response, credentials, username=tweet["username"])
                print(f"[REPLY] Replied to tweet by @{tweet['username']}: {response}")
