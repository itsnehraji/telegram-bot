from flask import Flask, request
import telegram
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
import os

# Bot token and channel username
TOKEN = "7947138227:AAEHCdSKjGrJYGteA8WP32urKDynXxfr4Qs"
CHANNEL_USERNAME = "@evidhyalaya_official"  # Replace with your actual channel username

bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return '🤖 Bot is live!'

@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        message_text = update.message.text

        if message_text == "/start":
            try:
                member_status = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id).status
                if member_status in ['member', 'administrator', 'creator']:
                    # ✅ User is a member
                    keyboard = [[
                        InlineKeyboardButton("📄 Download Practice Sheets", url="https://www.evidhyalaya.in/s/pages/bitsat2025-practice-sheets")
                    ]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    bot.send_message(
                        chat_id=chat_id,
                        text="🎉 *Thanks for joining!* \n\n✅ Now you can download your *Practice Sheets* below 👇",
                        reply_markup=reply_markup,
                        parse_mode=telegram.ParseMode.MARKDOWN
                    )
                else:
                    raise Exception("Not a member")
            except:
                # ❌ User is not a member
                keyboard = [[
                    InlineKeyboardButton("🔗 Join Our Telegram Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")
                ]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(
                    chat_id=chat_id,
                    text="⚠️ *Join our Telegram channel to download the Practice Sheets!*\n\n📢 Stay updated and access premium content!",
                    reply_markup=reply_markup,
                    parse_mode=telegram.ParseMode.MARKDOWN
                )
        else:
            bot.send_message(chat_id=chat_id, text="👋 Send /start to begin.")

        return 'OK'
    except Exception as e:
        print(f"Error: {e}")
        return 'Error', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
