from dotenv import load_dotenv
import os
import logging
import telebot
from telebot import types
from utils.netbox_utils.netbox import get_tag_netbox
# from utils.mikrotik_utils.mikrotik import get_info_mikrotik
from utils.huawei_utils.huawei import get_info_huawei
# from utils.dlink_utils.dlink import get_info_dlink
# from utils.snr_utils.snr import get_info_snr


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
    logging.info(get_tag_netbox(text.strip()))
    if text == "Назад":
        back_to_main_menu(bot, user_id)
        return
    if get_tag_netbox(text.strip()) == 'mikrotik':
        userid_states[user_id] = STATE_MIK_DIAG
    elif get_tag_netbox(text.strip()) == 'dlink':
        userid_states[user_id] = STATE_DLINK_DIAG
    elif get_tag_netbox(text.strip()) == 'huawei':
        userid_states[user_id] = STATE_HUAWEI_DIAG
    elif get_tag_netbox(text.strip()) == 'snr':
        userid_states[user_id] = STATE_SNR_DIAG
    else:
        bot.send_message(user_id, "Введите корректный IP-адрес")
        return

    userid_host[user_id] = text.strip()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Статусы физических интерфейсов")
    markup.add("Системная информация")
    markup.add("VLAN на интерфейсах")
    markup.add("Назад")
    bot.send_message(user_id, "Выберите действие: ", reply_markup=markup)
    

@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_MIK_DIAG)
def diagnostics_mik_handler(message):
    user_id = message.from_user.id
    text = message.text
    if text == "Назад":
        back_to_main_menu(bot, user_id)
        return
    bot.send_message(user_id, "Проверяю... Ждите")
    if text == "Статусы физических интерфейсов":
        logging.info(userid_host.get(user_id))
        host = userid_host.get(user_id)
        bot.send_message(user_id, get_info_mikrotik("int-info", host))
    elif text == "VLAN на интерфейсах":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_mikrotik("vlan-info", host))
    elif text == "Системная информация":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_mikrotik("system-info", host))
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_DLINK_DIAG)
def diagnostics_dlink_handler(message):
    user_id = message.from_user.id
    text = message.text
    if text == "Назад":
        back_to_main_menu(bot, user_id)
        return
    
    bot.send_message(user_id, "Проверяю... Ждите")
    if text == "Статусы физических интерфейсов":
        logging.info(userid_host.get(user_id))
        host = userid_host.get(user_id)
        bot.send_message(user_id, get_info_dlink("int-info", host))
    elif text == "VLAN на интерфейсах":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_dlink("vlan-info", host))
    elif text == "Системная информация":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_dlink("system-info", host))
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_HUAWEI_DIAG)
def diagnostics_huawei_handler(message):
    user_id = message.from_user.id
    text = message.text
    if text == "Назад":
        back_to_main_menu(bot, user_id)
        return
    
    bot.send_message(user_id, "Проверяю... Ждите")
    host = userid_host.get(user_id)
    if text == "Статусы физических интерфейсов":
        logging.info(userid_host.get(user_id))
        answer = get_info_huawei("int-info", host)
        if answer == None:
            bot.send_message(user_id, "Ошибка подключения. Администратор уведомлен. Переход в главное меню")
            logging.error(f"Ошибка подключения к {host} в ConnectHandler huawei.py")
            back_to_main_menu(bot, user_id)
            return
        else:
            bot.send_message(user_id, answer)
    elif text == "VLAN на интерфейсах":
        logging.info(userid_host.get(user_id))
        answer = get_info_huawei("vlan-info", host)
        if answer == None:
            bot.send_message(user_id, "Ошибка подключения. Администратор уведомлен. Переход в главное меню")
            logging.error(f"Ошибка подключения к {host} в ConnectHandler huawei.py")
            back_to_main_menu(bot, user_id)
            return
        else:
            bot.send_message(user_id, answer)
    elif text == "Системная информация":
        logging.info(userid_host.get(user_id))
        answer = get_info_huawei("system-info", host)
        if answer == None:
            bot.send_message(user_id, "Ошибка подключения. Администратор уведомлен. Переход в главное меню")
            logging.error(f"Ошибка подключения к {host} в ConnectHandler huawei.py")
            back_to_main_menu(bot, user_id)
            return
        else:
            bot.send_message(user_id, answer)
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


@bot.message_handler(func=lambda msg: userid_states.get(msg.from_user.id) == STATE_SNR_DIAG)
def diagnostics_snr_handler(message):
    user_id = message.from_user.id
    text = message.text
    if text == "Назад":
        back_to_main_menu(bot, user_id)
        return
    elif text == "":
        pass
    bot.send_message(user_id, "Проверяю... Ждите")
    if text == "Статусы физических интерфейсов":
        logging.info(userid_host.get(user_id))
        host = userid_host.get(user_id)
        bot.send_message(user_id, get_info_snr("int-info", host))
    elif text == "VLAN на интерфейсах":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_snr("vlan-info", host))
    elif text == "Системная информация":
        logging.info(userid_host.get(user_id))
        bot.send_message(user_id, get_info_snr("system-info", host))
    else:
        bot.send_message(user_id, "Пожалуйста, воспользуйтесь кнопками")


def back_to_main_menu(bot, user_id):
    userid_states[user_id] = STATE_MAIN_MENU
    bot.send_message(user_id, "Возврат в главное меню")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Диагностика")
    markup.add(btn)
    bot.send_message(user_id, "Выберите действие: ", reply_markup=markup)


@bot.message_handler(func=lambda msg: True)
def fallback_handler(message):
    user_id = message.from_user.id
    logging.info(f"Неизвестное состояние пользователя {user_id}. Возврат в главное меню.")
    userid_states[user_id] = STATE_MAIN_MENU
    userid_host.pop(user_id, None)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Диагностика")
    markup.add(btn)
    bot.send_message(user_id, "Был перезапуск бота. Вы возвращены в главное меню", reply_markup=markup)

bot.polling()