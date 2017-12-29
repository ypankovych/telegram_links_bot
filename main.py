import telebot
import requests
import traceback
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool

token = ''
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help'])
def help(message):
    with open('help.txt') as help_message:
        bot.send_message(chat_id=message.from_user.id, text=help_message.read())

@bot.message_handler(content_types=['text'])
def messages_handler(message):
    with ThreadPool(100) as pool:
        pool.map(check, [[x, message.from_user.id] for x in message.text.split() if not x.startswith('/')])

def check(links):
    data = requests.get(f'https://t.me/{links[0][1:]}', timeout = 1000).text
    soup_object = BeautifulSoup(data, 'html.parser')
    try:
        if not soup_object.find('i', class_='tgme_icon_user'):
            if soup_object.find('a', 'tgme_action_button_new').text == 'Send Message':
                result = f'✅ {links[0]}: (*User*)'
            else:
                result = f'✅ {links[0]}: (*{soup_object.find("a", class_="tgme_action_button_new").text.split()[1]}*)'
        else:
            result = f'❌ {links[0]}: (*Not found*)'
        bot.send_message(chat_id=links[1], text=result, parse_mode='Markdown')
    except Exception:
        print(traceback.format_exc())

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
