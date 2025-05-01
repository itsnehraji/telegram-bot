from flask import Flask, request
import telegram
import os

TOKEN = "7947138227:AAEHCdSKjGrJYGteA8WP32urKDynXxfr4Qs"
CHANNEL_USERNAME = "@evidhyalaya_official"  # Replace with your actual channel username

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f"/webhook/{TOKEN}", methods=['POST'])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        message = update.message
        chat_id = message.chat.id

        # Check if user is a member of the channel
        member = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=chat_id)
        status = member.status  # 'creator', 'administrator', 'member', 'left', 'kicked'

        if status in ['member', 'administrator', 'creator']:
            bot.send_message(chat_id=chat_id, text="✅ You are a verified member! Here's your content...")
        else:
            bot.send_message(chat_id=chat_id, text="🚫 Please join our channel first:\nhttps://t.me/evidhyalaya_official")
    except Exception as e:
        print(f"Error: {e}")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
