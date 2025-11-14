from dotenv import load_dotenv
import os
import logging
import telebot
from telebot import types


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/file.log",
    filemode='a'
)

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
user_states = {}
STATE_MAIN_MENU = 'main_menu'
STATE_DIAGNOSTICS = 'diagnostics'
STATE_TICKETS = 'tickets'

# MAIN LOGIC 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для диагностики сетевого оборудования!")
    user_id = message.from_user.id
    user_states[user_id] = STATE_MAIN_MENU

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Диагностика")
    btn2 = types.KeyboardButton("Заявки")
    markup.add(btn1, btn2)

    bot.send_message(user_id, "Выберите действие: ", reply_markup=markup)





@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ты написал: {message.text}")

bot.polling()