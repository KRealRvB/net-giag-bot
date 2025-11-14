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

# MAIN MENU
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


# MAIN MANU HANDLER
@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == STATE_MAIN_MENU)
def main_menu_handler(message):
    user_id = message.from_user.id
    text = message.text

    if text == "Диагностика":
        user_states[user_id] = STATE_DIAGNOSTICS
        bot.send_message(user_id, "Введите ip-адрес устройства, например 192.168.0.1")

        
    elif text == "Заявки":
        tickets = ["Заявка 1", "Заявка 2", "Заявка 3"]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for t in tickets:
            markup.add(t)
        markup.add("Назад")
        bot.send_message(user_id, "Выберите заявку: ", reply_markup=markup)

    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")
bot.polling()