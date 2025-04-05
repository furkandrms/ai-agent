import tweepy
import os
from dotenv import load_dotenv
import json

load_dotenv()

CALLBACK_URL = os.getenv("CALLBACK_URL")
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
OAUTH_MAP_PATH = "oauth_token_map.json"

def save_token_map(token, data):
    try:
        if os.path.exists(OAUTH_MAP_PATH):
            with open(OAUTH_MAP_PATH, "r") as f:
                mapping = json.load(f)
        else:
            mapping = {}

        mapping[token] = data

        with open(OAUTH_MAP_PATH, "w") as f:
            json.dump(mapping, f)
    except Exception as e:
        print("[ERROR] Token map failed to save:", e)

def get_auth_url(config_path):
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, CALLBACK_URL)
    try:
        auth_url = auth.get_authorization_url()
        token = auth.request_token["oauth_token"]

        save_token_map(token, {
            "oauth_token_secret": auth.request_token["oauth_token_secret"],
            "config_path": config_path
        })

        return auth_url
    except Exception as e:
        print("[ERROR] Auth URL could not be retrieved:", e)
        return None

def get_access_tokens(request_token, oauth_verifier):
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET)
    auth.request_token = request_token
    return auth.get_access_token(oauth_verifier)
