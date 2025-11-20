from dotenv import load_dotenv
import os
import logging
import telebot
from telebot import types
from utils.netbox_utils.netbox import get_tag_netbox, get_role_netbox
from utils.mikrotik_utils.mikrotik import get_info_mikrotik
from utils.huawei_utils.huawei import get_info_huawei
from utils.dlink_utils.dlink import get_info_dlink
from utils.snr_utils.snr import get_info_snr


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
STATE_MIK_DIAG = 'mik_diag'
STATE_DLINK_DIAG = 'dlink_diag'
STATE_HUAWEI_DIAG = 'huawei_diag'
STATE_SNR_DIAG = 'snr_diag'

# MAIN LOGIC 

# MAIN MENU
@bot.message_handler(commands=['start'])
def main_menu(message):
    bot.reply_to(message, "Привет! Я бот для диагностики сетевого оборудования!")
    user_id = message.from_user.id
    userid_states[user_id] = STATE_MAIN_MENU

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Диагностика")
    markup.add(btn)

    bot.send_message(user_id, "Выберите действие: ", reply_markup=markup)


# MAIN MANU HANDLER
@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_MAIN_MENU)
def main_menu_handler(message):
    user_id = message.from_user.id
    text = message.text

    if text == "Диагностика":
        userid_states[user_id] = STATE_DIAGNOSTICS
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Назад")
        bot.send_message(user_id, "Введите ip-адрес устройства, например 192.168.0.1")
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


# DIAG HANDLER
@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_DIAGNOSTICS)
def diagnostics_handler(message):
    user_id = message.from_user.id
    text = message.text
    if get_tag_netbox(text.strip()) == 'mikrotik' or get_role_netbox(text.strip()) == 'loopback':
        userid_states[user_id] = STATE_MIK_DIAG
    elif get_tag_netbox(text.strip()) == 'dlink':
        userid_states[user_id] = STATE_DLINK_DIAG
    elif get_tag_netbox(text.strip()) == 'huawei':
        userid_states[user_id] = STATE_HUAWEI_DIAG
    elif get_tag_netbox(text.strip()) == 'snr':
        userid_states[user_id] = STATE_SNR_DIAG

    userid_host[user_id] = text.strip()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Статусы физических интерфейсов")
    markup.add("Системная информация")
    markup.add("VLAN на интерфейсах")
    markup.add("Назад")
    bot.send_message(user_id, "Выберете действие: ", reply_markup=markup)
    if text == "Назад":
        return main_menu(message)
    else:
        pass # если это не IP-адрес, то переспрашиваем
        bot.send_message(user_id, "Пожалуйста, введите корректный IP-адрес, либо кнопку 'Назад'")


@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_MIK_DIAG)
def diagnostics_mik_handler(message):
    user_id = message.from_user.id
    text = message.text
    bot.send_message(user_id, "Получаю... Ждите")
    if text == "Статусы физических интерфейсов":
        logging.info(userid_host.get(user_id))
        host = userid_host.get(user_id)
        bot.send_message(user_id, get_info_mikrotik("int-info", host))
    if text == "VLAN на интерфейсах":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_mikrotik("vlan-info", host))
    if text == "Системная информация":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_mikrotik("system-info", host))
    elif text == "Назад":
        return main_menu(message)
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_DLINK_DIAG)
def diagnostics_mik_handler(message):
    user_id = message.from_user.id
    text = message.text
    bot.send_message(user_id, "Получаю... Ждите")
    if text == "Статусы физических интерфейсов":
        logging.info(userid_host.get(user_id))
        host = userid_host.get(user_id)
        bot.send_message(user_id, get_info_dlink("int-info", host))
    if text == "VLAN на интерфейсах":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_dlink("vlan-info", host))
    if text == "Системная информация":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_dlink("system-info", host))
    elif text == "Назад":
        return main_menu(message)
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_HUAWEI_DIAG)
def diagnostics_mik_handler(message):
    user_id = message.from_user.id
    text = message.text
    bot.send_message(user_id, "Получаю... Ждите")
    if text == "Статусы физических интерфейсов":
        logging.info(userid_host.get(user_id))
        host = userid_host.get(user_id)
        bot.send_message(user_id, get_info_huawei("int-info", host))
    if text == "VLAN на интерфейсах":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_huawei("vlan-info", host))
    if text == "Системная информация":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_huawei("system-info", host))
    elif text == "Назад":
        return main_menu(message)
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_SNR_DIAG)
def diagnostics_mik_handler(message):
    user_id = message.from_user.id
    text = message.text
    bot.send_message(user_id, "Получаю... Ждите")
    if text == "Статусы физических интерфейсов":
        logging.info(userid_host.get(user_id))
        host = userid_host.get(user_id)
        bot.send_message(user_id, get_info_snr("int-info", host))
    if text == "VLAN на интерфейсах":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_snr("vlan-info", host))
    if text == "Системная информация":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_snr("system-info", host))
    elif text == "Назад":
        return main_menu(message)
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")

bot.polling()