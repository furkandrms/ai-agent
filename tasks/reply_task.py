from tasks.base_task import BaseTask
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from utils.twitter_api import get_recent_mentions, reply_to_tweet
from utils.twitter_api import get_user_client
from tweet_cache import get_cached_mentions, update_cached_mentions

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
            client = get_user_client(credentials["access_token"], credentials["access_secret"])
            me = client.get_me()
            user_id = me.data.id if me.data else None
            if not user_id:
                print("[ERROR] Failed to get user ID.")
                return

            mentions = get_cached_mentions(user_id)
            if not mentions:
                response = client.get_users_mentions(id=user_id, max_results=5)
                if not response.data:
                    print("[WARNING] No mentions found.")
                    return
                mentions = [mention.data for mention in response.data]
                update_cached_mentions(user_id, mentions)
            else:
                print("[CACHE] Mentionlar önbellekten yüklendi.")

        except TooManyRequests as e:
            print("[RATE LIMIT] Mention çekimi limitlendi. Daha sonra tekrar denenecek.")
            time.sleep(60)
            return 

        for tweet in mentions: 
            text = tweet["text"]
            if any(kw.lower() in text.lower() for kw in keywords): 
                print(f"[MATCH] Keyword matched in tweet: {text}")

                prompt_template = PromptTemplate.from_template(
                    "Reply to this tweet in a {tone} and {style} way about {topic}:\\n\\n\\\"{tweet}\\\""
                )

                llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.7, max_tokens=100)
                chain = prompt_template | llm

                response = chain.invoke({
                    "tone": personality["tone"],
                    "style": personality["style"],
                    "topic": personality["topic"],
                    "tweet": text
                }).content

                reply_to_tweet(tweet["id"], response, credentials, username=tweet["username"])
                print(f"[REPLY] Replied to tweet by @{tweet['username']}: {response}")