def post_tweet(tweet): 
    print(f"[MOCK] Posting tweet: \n{tweet}\n")

def get_recent_mentions():
    print("[MOCK] Getting recent mentions")
    return [
        {
            "id": 1,
            "text": "Hey @zen_bot, can you help me with my homework?"
        },
        {
            "id": 2,
            "text": "I'm feeling sad today, @zen_bot can you cheer me up?"
        }
    ]

def reply_to_tweet(tweet_id, reply):
    print(f"[MOCK] Replying to tweet {tweet_id} with response: \n{reply}\n")
