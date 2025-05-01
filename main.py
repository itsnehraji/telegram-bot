import os
from flask import Flask, request
import requests

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@evidhyalaya_official"  # your Telegram channel

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_id = data["message"]["from"]["id"]

        # Check membership
        res = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember",
            params={"chat_id": CHANNEL_USERNAME, "user_id": user_id}
        ).json()

        status = res.get("result", {}).get("status", "")
        if status in ["member", "creator", "administrator"]:
            message = "✅ You have access to the sheets!"
        else:
            message = "❌ Please join our channel first: https://t.me/evidhyalaya_official"

        # Send reply
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": message}
        )

    return "OK"
