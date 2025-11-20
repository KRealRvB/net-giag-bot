from dotenv import load_dotenv
import os
import logging
import telebot
from telebot import types
from utils.netbox_utils.netbox import get_tag_netbox
from utils.mikrotik_utils.mikrotik import get_if_info_mikrotik


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs/file.log",
    filemode='a'
)

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
userid_states = {}
userid_host = {}
STATE_MAIN_MENU = 'main_menu'
STATE_DIAGNOSTICS = 'diagnostics'
STATE_TICKETS = 'tickets'
STATE_MIK_DIAG = 'mik_diag'

# MAIN LOGIC 

# MAIN MENU
@bot.message_handler(commands=['start'])
def main_menu(message):
    bot.reply_to(message, "Привет! Я бот для диагностики сетевого оборудования!")
    user_id = message.from_user.id
    userid_states[user_id] = STATE_MAIN_MENU

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Диагностика")
    btn2 = types.KeyboardButton("Заявки")
    markup.add(btn1, btn2)

    bot.send_message(user_id, "Выберите действие: ", reply_markup=markup)


# MAIN MANU HANDLER
@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_MAIN_MENU)
def main_menu_handler(message):
    user_id = message.from_user.id
    text = message.text

    if text == "Диагностика":
        userid_states[user_id] = STATE_DIAGNOSTICS
        bot.send_message(user_id, "Введите ip-адрес устройства, например 192.168.0.1")

        
    # elif text == "Заявки":
    #     userid_states[user_id] = STATE_TICKETS
    #     tickets = ["Заявка 1", "Заявка 2", "Заявка 3"]
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     for t in tickets:
    #         markup.add(t)
    #     markup.add("Назад")
    #     bot.send_message(user_id, "Выберите заявку: ", reply_markup=markup)

    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


# DIAG HANDLER
@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_DIAGNOSTICS)
def diagnostics_handler(message):
    user_id = message.from_user.id
    text = message.text
    if get_tag_netbox(text.strip()):
        userid_host[user_id] = text.strip()
        userid_states[user_id] = STATE_MIK_DIAG
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Статусы физических интерфейсов")
        markup.add("Назад")
        bot.send_message(user_id, "Выберете действие: ", reply_markup=markup)
    elif text == "Назад":
        return main_menu(message)
    else:
        pass # если это не IP-адрес, то переспрашиваем
        bot.send_message(user_id, "Пожалуйста, введите корректный IP-адрес, либо кнопку 'Назад'")


@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_MIK_DIAG)
def diagnostics_mik_handler(message):
    user_id = message.from_user.id
    text = message.text
    if text == "Статусы физических интерфейсов":
        bot.send_message(user_id, "Получаю... Ждите")
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_if_info_mikrotik(userid_host.get(user_id)))
    elif text == "Назад":
        return main_menu(message)
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


# @bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_TICKETS)
# def tickets_handler(message):
#     user_id = message.from_user.id
#     bot.send_message(user_id, "Информация по заявке... Пока ничего нет. Возврат в главное...")
#     return main_menu(message)
bot.polling()