import threading
import re
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- LOAD ML MODEL ---
model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

app = Flask(__name__)
CORS(app)


# --- HYBRID SPAM DETECTION ENGINE ---
def check_message(text):
    if not text or len(text.strip()) < 3:
        return "Safe"

    msg = text.lower()

    # -------------------------------
    # 1. TRUSTED SAFE LIST
    # -------------------------------
    trusted_entities = [
        'nptel', 'iitm', 'swayam', 'infosys', 'hackwithinfy',
        'tcs', 'otp', 'exam', 'hall ticket', 'admit card',
        'placement office', 'placement cell', 'verification code'
        ,'meeting'
    ]

    if any(entity in msg for entity in trusted_entities):
        return "Safe"

    # -------------------------------
    # 2. STRONG SPAM RULES
    # -------------------------------
    spam_keywords = [
        'win', 'winner', 'prize', 'free', 'bonus',
        'offer', 'urgent', 'claim', 'money', 'cash',
        'lottery', 'congratulations', 'click here',
        'limited offer', 'earn', 'income'
    ]

    has_spam_words = any(word in msg for word in spam_keywords)

    has_link = bool(re.search(r'(http|www|bit\.ly|forms\.gle)', msg))

    if has_spam_words or has_link:
        return "Spam"

    # -------------------------------
    # 3. ML PREDICTION (FINAL LAYER)
    # -------------------------------
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]

    if prediction == 1:
        return "Spam"

    return "Safe"


# --- FLASK API ---
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    label = check_message(text)
    return jsonify({"label": label})


# --- TELEGRAM BOT ---
async def handle_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    label = check_message(user_text)

    if label == "Spam":
        await update.message.reply_text("🚨 Spam")
    else:
        await update.message.reply_text("✅ Safe")


def run_bot():
    TOKEN = "8377037779:AAGxYKtbOAuZrU0_Y6aFCZaz-wb-q-eE3F0"

    application = Application.builder().token(TOKEN).build()
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram)
    )

    print("🤖 Telegram Bot: Active")
    application.run_polling(close_loop=False)


# --- MAIN ---
if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()

    print("🌐 Flask Server running at http://127.0.0.1:5000")
    app.run(port=5000, debug=False, use_reloader=False)