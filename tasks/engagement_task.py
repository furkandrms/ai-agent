from tasks.base_task import BaseTask
from utils.twitter_api import get_user_client
from utils.twitter_api import like_tweet, retweet, follow_user


from dotenv import load_dotenv
import os

load_dotenv()

class EngagementTask(BaseTask):
    def execute(self, personality, config=None):
        credentials = config.get("twitter_credentials") if config else None
        if not credentials:
            print("[ERROR] Twitter credentials not found in config.")
            return
        
        keywords = self.config.get("keywords", [])
        actions = self.config.get("actions", [])

        client= get_user_client(credentials["access_token"], credentials["access_secret"])
        if not client:
            print("[ERROR] Failed to create Twitter client.")
            return

        me = client.get_me()
        user_id = me.data.id if me.data else None
        if not user_id:
            print("[ERROR] Failed to get user ID.")
            return
        
        tweets = client.get_users_tweets(id=user_id, max_results=5)

        if not tweets.data:
            print("[WARNING] No tweets found.")
            return
        
        for tweet in tweets.data:
            if any (kw.lower() in tweet.text.lower() for kw in keywords): 
                print(f"[MATCH] Keyword matched in tweet: {tweet.text}")
                
                for action in actions:
                    if action == "like":
                        like_tweet(tweet.id, credentials)
                    elif action == "retweet":
                        retweet(tweet.id, credentials)
                    elif action == "follow":
                        follow_user(tweet.author_id, credentials)
                    else:
                        print(f"[WARNING] Unknown action: {action}")

