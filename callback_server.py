# callback_server.py

from flask import Flask, request
from auth.twitter_auth import get_access_tokens, REQUEST_TOKENS

app = Flask(__name__)

@app.route("/callback")
def callback():
    oauth_token = request.args.get("oauth_token")
    oauth_verifier = request.args.get("oauth_verifier")

    # DEV: test için token'ı manuel veriyoruz
    session_id = "demo"
    REQUEST_TOKENS[session_id] = {
        "oauth_token": oauth_token,
        "oauth_token_secret": "GEÇİCİ_OLARAK_ELLE_EKLE"  # bunu doğru değerle eşle
    }

    access_token, access_secret = get_access_tokens(session_id, oauth_verifier)

    if access_token and access_secret:
        return f"""
        ✅ Twitter hesabınız bağlandı!<br><br>
        <b>Access Token:</b> {access_token}<br>
        <b>Access Secret:</b> {access_secret}<br>
        Bunları config dosyanıza manuel ekleyebilirsiniz.
        """, 200
    else:
        return "❌ Access token alınamadı.", 400

if __name__ == "__main__":
    app.run(port=8000, debug=True)
