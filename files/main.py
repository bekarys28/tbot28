import telebot
from telebot import types
from flask import Flask, request
import os

TOKEN = "7341048260:AAGOCYHUW9AMqQL_TVVtF3IzhuAo4cIFiwc"  # Вставь сюда свой токен

bot = telebot.TeleBot(TOKEN)

STUDENT_NAME = "Aitas Bekarys"

app = Flask(__name__)

# Main menu keyboard
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📚 Student Name")
    btn2 = types.KeyboardButton("📄 Stuff Document")
    btn3 = types.KeyboardButton("📊 Picture")
    markup.add(btn1, btn2, btn3)
    return markup

# Back to menu keyboard
def back_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_btn = types.KeyboardButton("🔙 Back to Menu")
    markup.add(back_btn)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome! Choose an option:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "📚 Student Name")
def send_name(message):
    bot.send_message(message.chat.id, f"Student Name: {STUDENT_NAME}", reply_markup=back_menu())

@bot.message_handler(func=lambda message: message.text == "📄 Stuff Document")
def send_word(message):
    try:
        with open("student_info.docx", "rb") as doc:
            bot.send_document(message.chat.id, doc, reply_markup=back_menu())
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Word document not found!", reply_markup=back_menu())

@bot.message_handler(func=lambda message: message.text == "📊 Picture")
def send_presentation(message):
    try:
        with open("presentation2.pdf", "rb") as ppt:
            bot.send_document(message.chat.id, ppt, reply_markup=back_menu())
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Presentation not found!", reply_markup=back_menu())

@bot.message_handler(func=lambda message: message.text == "🔙 Back to Menu")
def back_to_menu(message):
    bot.send_message(message.chat.id, "Back to main menu:", reply_markup=main_menu())

# Webhook
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_update = request.get_json()
    update = telebot.types.Update.de_json(json_update)
    bot.process_new_updates([update])
    return '', 200

@app.route("/", methods=["GET"])
def home():
    return "Бот работает!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://ТВОЙ_RAILWAY_URL")  # Замени на свой Railway URL
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
