from flask import Flask, request
import telegram
import os

TOKEN = "YOUR_BOT_TOKEN"  # Replace this with your actual token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@app.route(f"/webhook/{TOKEN}", methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message = update.message.text

    # Simple echo bot
    bot.send_message(chat_id=chat_id, text=f"You said: {message}")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render requires this
    app.run(host="0.0.0.0", port=port)
