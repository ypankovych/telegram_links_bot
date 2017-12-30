import botan
import telebot
import requests
import traceback
from bs4 import BeautifulSoup
from config import token, botan_key
from multiprocessing.pool import ThreadPool

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help', 'start'])
def help(message):
    with open('help.txt') as help_message:
        bot.send_message(chat_id=message.from_user.id, text=help_message.read())
        botan.track(botan_key, message.chat.id, message, 'Start bot')

@bot.message_handler(content_types=['text'])
def messages_handler(message):
    with ThreadPool(100) as pool:
        pool.map(check, [[x, message] for x in message.text.split() if not x.startswith('/')])

def check(links):
    data = requests.get(f'https://t.me/{links[0][1:]}', timeout = 1000).text
    soup_object = BeautifulSoup(data, 'html.parser')
    try:
        if not soup_object.find('i', class_='tgme_icon_user'):
            if soup_object.find('a', 'tgme_action_button_new').text == 'Send Message':
                result = f'✅ {links[0]}: (<b>User</b>)'
            else:
                result = f'✅ {links[0]}: (<b>{soup_object.find("a", class_="tgme_action_button_new").text.split()[1]}</b>)'
        else:
            result = f'❌ {links[0]}: (<b>Not found</b>)'
        bot.send_message(chat_id=links[1].chat.id, text=result, parse_mode='HTML')
        botan.track(botan_key, links[1].chat.id, links[1], f'Checked username: {links[0]}')
    except Exception:
        print(traceback.format_exc())
        bot.send_message(chat_id=links[1].chat.id, text=f'Invalid username {links[0]}.')
