import tweepy
import os
import json
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

LOG_FILE = "twitter_log.json"

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")


def get_user_client(twitter_access_token, twitter_access_token_secret):

    return tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret
    )


def log_tweet(text, tweet_id, type_="tweet", related_to=None):
    log_data = {
        "id": str(tweet_id),
        "type": type_,
        "text": text,
        "related_to": related_to,
        "url": f"https://twitter.com/user/status/{tweet_id}"
    }

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)

    except Exception as e:
        print(f"[ERROR] Failed to log tweet: {e}")


def post_tweet(tweet, credentials):
    if is_duplicate(tweet):
        print("[SKIP] Tweet is skipped because it has similar content.")
        return

    try:
        client = get_user_client(credentials["access_token"], credentials["access_secret"])
        response = client.create_tweet(text=tweet)

        tweet_id = response.data.get("id")
        print(f"[REAL] Tweet posted: {tweet}")
        log_tweet(tweet, tweet_id, "tweet")

    except Exception as e:
        print(f"[ERROR] Failed to post tweet: {e}")



def get_recent_mentions(credentials, user_id=None, limit=5):
    try:
        client = get_user_client(credentials["access_token"], credentials["access_secret"])

        if not user_id:
            user_response = client.get_me()
            user_id = user_response.data.id

        mentions = client.get_users_mentions(id=user_id, max_results=limit)
        results = []

        if mentions.data:
            for tweet in mentions.data:
                results.append({
                    "id": str(tweet.id),
                    "text": tweet.text,
                    "username": None
                })
        return results

    except Exception as e:
        print(f"[ERROR] Failed to fetch mentions: {e}")
        return []


def reply_to_tweet(tweet_id, reply_text, credentials, username=None):
    full_text = f"@{username} {reply_text}" if username else reply_text

    try:
        client = get_user_client(credentials["access_token"], credentials["access_secret"])
        response = client.create_tweet(
            text=full_text,
            in_reply_to_tweet_id=tweet_id
        )
        print(f"[REAL] Replied to tweet {tweet_id} with: {full_text}")
        log_tweet(full_text, response.data.get("id"), "reply", related_to=tweet_id)

    except Exception as e:
        print(f"[ERROR] Failed to reply: {e}")

def like_tweet(tweet_id, credentials):
    try: 
        client = get_user_client(credentials["access_token"], credentials["access_secret"])
        response = client.like(tweet_id)
        print(f"[REAL] Liked tweet {response.data.get('id')}")
        log_tweet(tweet_id, tweet_id, "like", related_to=tweet_id)
    except Exception as e:
        print(f"[ERROR] Failed to like tweet: {e}")

def retweet(tweet_id, credentials): 
    try: 
        client = get_user_client(credentials["access_token"], credentials["access_secret"])
        response = client.retweet(tweet_id)
        print(f"[REAL] Retweeted tweet {response.data.get('id')}")
        log_tweet(tweet_id, tweet_id, "retweet", related_to=tweet_id)
    except Exception as e:
        print(f"[ERROR] Failed to retweet: {e}")

def follow_user(user_id, credentials):
    try:
        client = get_user_client(credentials["access_token"], credentials["access_secret"])
        client.follow_user(target_user_id=user_id)
        print(f"[FOLLOW] Kullanıcı {user_id} takip edildi.")
    except Exception as e:
        print(f"[ERROR] Failed to follow user {user_id}: {e}")

def is_duplicate(text, threshold=0.9):
    try:
        if not os.path.exists(LOG_FILE):
            return False

        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

        for entry in logs[-20:]:
            similarity = SequenceMatcher(None, entry["text"], text).ratio()
            if similarity >= threshold:
                return True
        return False

    except Exception as e:
        print(f"[ERROR] Duplicate check failed: {e}")
        return False
