from flask import Flask, request
from auth.twitter_auth import get_access_tokens
import json
import os

app = Flask(__name__)

OAUTH_MAP_PATH = "oauth_token_map.json"

def get_mapping(oauth_token):
    try:
        if not os.path.exists(OAUTH_MAP_PATH):
            return None
        with open(OAUTH_MAP_PATH, "r") as f:
            mapping = json.load(f)
        return mapping.get(oauth_token, None)
    except Exception as e:
        print(f"[ERROR] Failed to read mapping file: {e}")
        return None

@app.route("/callback")
def callback():
    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")

    print(f"[CALLBACK] oauth_token: {oauth_token}")
    print(f"[CALLBACK] oauth_verifier: {oauth_verifier}")

    mapping = get_mapping(oauth_token)
    if not mapping:
        print(f"[ERROR] No mapping found for token: {oauth_token}")
        return "❌ Token mapping not found", 400

    request_token = {
        "oauth_token": oauth_token,
        "oauth_token_secret": mapping["oauth_token_secret"]
    }

    try:
        access_token, access_secret = get_access_tokens(request_token, oauth_verifier)
    except Exception as e:
        print(f"❌ Failed to receive access token: {e}")
        return f"❌ Failed to receive access token: {e}", 500

    config_path = mapping["config_path"]

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        config["twitter_credentials"] = {
            "access_token": access_token,
            "access_secret": access_secret
        }

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"[SUCCESS] Token information was written to {config_path}.")

        return f"""✅ Your Twitter account is connected!<br><br>
        Token information was automatically written to the <b>{config_path}</b> file.
        """, 200

    except Exception as e:
        print(f"[ERROR] File operation failed: {e}")
        return f"Failed to write to file: {e}", 500

if __name__ == "__main__":
    app.run(port=8000, debug=True)
