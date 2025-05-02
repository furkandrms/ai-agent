
import os
import json
import time
from datetime import datetime, timedelta

CACHE_FILE = "tweet_cache.json"
CACHE_DURATION = 15 * 60  # 15 dakika

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(cache_data):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f, indent=2)

def get_cached_tweets(user_id):
    cache = load_cache()
    user_data = cache.get(str(user_id))
    if not user_data:
        return None
    timestamp = user_data.get("timestamp")
    if not timestamp:
        return None
    ts = datetime.fromisoformat(timestamp)
    if datetime.now() - ts < timedelta(seconds=CACHE_DURATION):
        return user_data.get("tweets", [])
    return None

def update_cached_tweets(user_id, tweets):
    cache = load_cache()
    cache[str(user_id)] = {
        "timestamp": datetime.now().isoformat(),
        "tweets": tweets
    }
    save_cache(cache)
    
def get_cached_mentions(user_id):
    cache = load_cache()
    user_data = cache.get(f"mentions_{user_id}")
    if not user_data:
        return None
    timestamp = user_data.get("timestamp")
    if not timestamp:
        return None
    ts = datetime.fromisoformat(timestamp)
    if datetime.now() - ts < timedelta(seconds=CACHE_DURATION):
        return user_data.get("mentions", [])
    return None

def update_cached_mentions(user_id, mentions):
    cache = load_cache()
    cache[f"mentions_{user_id}"] = {
        "timestamp": datetime.now().isoformat(),
        "mentions": mentions
    }
    save_cache(cache)