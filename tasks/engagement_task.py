from tasks.base_task import BaseTask
from utils.twitter_api import get_user_client
from utils.twitter_api import like_tweet, retweet, follow_user

from tweet_cache import get_cached_tweets, update_cached_tweets

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

        client = get_user_client(credentials["access_token"], credentials["access_secret"])
        if not client:
            print("[ERROR] Failed to create Twitter client.")
            return

        me = client.get_me()
        user_id = me.data.id if me.data else None
        if not user_id:
            print("[ERROR] Failed to get user ID.")
            return

        tweets_data = get_cached_tweets(user_id)

        if not tweets_data:
            tweets = client.get_users_tweets(id=user_id, max_results=5)
            if not tweets.data:
                print("[WARNING] No tweets found.")
                return
            tweets_data = [tweet.data for tweet in tweets.data]
            update_cached_tweets(user_id, tweets_data)
        else:
            print("[CACHE] Tweetler önbellekten yüklendi.")

        for tweet in tweets_data:
            if any(kw.lower() in tweet['text'].lower() for kw in keywords):
                print(f"[MATCH] Keyword matched in tweet: {tweet['text']}")

                for action in actions:
                    if action == "like":
                        like_tweet(tweet['id'], credentials)
                    elif action == "retweet":
                        retweet(tweet['id'], credentials)
                    elif action == "follow":
                        follow_user(tweet['author_id'], credentials)