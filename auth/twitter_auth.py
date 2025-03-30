# auth/twitter_oauth.py

import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

CALLBACK_URL = os.getenv("CALLBACK_URL")
if CALLBACK_URL is None:
    raise ValueError("CALLBACK_URL is not set in .env file")
else:
    print("[INFO] Callback URL found")

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")

# Oturum için global dict
REQUEST_TOKENS = {}

def get_auth_url(session_id):
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, CALLBACK_URL)
    try:
        redirect_url = auth.get_authorization_url()
        REQUEST_TOKENS[session_id] = {
            "oauth_token": auth.request_token["oauth_token"],
            "oauth_token_secret": auth.request_token["oauth_token_secret"]
        }
        return redirect_url
    except Exception as e:
        print("Auth URL alınamadı:", e)
        return None
        

def get_access_tokens(session_id, oauth_verifier):
    if session_id not in REQUEST_TOKENS:
        return None, None

    request_token = REQUEST_TOKENS[session_id]
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET)
    auth.request_token = request_token

    try:
        access_token, access_secret = auth.get_access_token(oauth_verifier)
        return access_token, access_secret
    except Exception as e:
        print("Access token alınamadı:", e)
        return None, None
