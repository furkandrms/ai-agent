import tweepy
import os
from dotenv import load_dotenv

load_dotenv()


def get_user_api(access_token, access_secret):
    auth = tweepy.OAuth1UserHandler(
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_SECRET"),
        access_token,
        access_secret
    )
    return tweepy.API(auth)


def post_tweet(tweet, credentials):
    api = get_user_api(credentials["access_token"], credentials["access_secret"])
    api.update_status(tweet)


def get_recent_mentions(credentials, limit=5):
    try:
        api = get_user_api(credentials["access_token"], credentials["access_secret"])
        mentions = api.mentions_timeline(count=limit)
        results = []
        for tweet in mentions:
            results.append({
                "id": tweet.id_str,
                "text": tweet.text,
                "username": tweet.user.screen_name
            })
        return results
    except Exception as e:
        print(f"[ERROR] Failed to fetch mentions: {e}")
        return []


def reply_to_tweet(tweet_id, reply_text, credentials):
    try:
        api = get_user_api(credentials["access_token"], credentials["access_secret"])
        api.update_status(
            status=reply_text,
            in_reply_to_status_id=tweet_id,
            auto_populate_reply_metadata=True
        )
        print(f"[REAL] Replied to tweet {tweet_id} with: {reply_text}")
    except Exception as e:
        print(f"[ERROR] Failed to reply: {e}")
