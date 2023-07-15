import telebot
from telebot import types
import os
import random
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


def new_password(size_of_password):
    password = ''
    chars = '1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ+-*/.,=_([{|}])!?&@#%$^'
    for i in range(size_of_password):
        password += random.choice(chars)
        # password = f'{password}{chars[random.randint(0,len(chars)-1)]}'
    return password


def send(id, text):
    bot.send_message(chat_id=id, text=text)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row('Привет', 'Пока')
    keyboard.row('Как дела?')
    keyboard.row('Сгенерировать пароль')

    bot.send_message(chat_id=message.chat.id, text=f'Привет {message.from_user.first_name}!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def main_menu(message):

    chat_id = message.chat.id
    msg = message.text
    try:
        msg = int(msg)
    except:
        pass


    if msg == 'Привет':
        send(chat_id, 'И тебе привет! 😁')

    elif msg == 'Пока':
        send(chat_id, 'Уже уходишь? 😒')

    elif msg == 'Как дела?':
        send(chat_id, 'Всё хорошо 👍')

    elif msg == 'Сгенерировать пароль':
        send(chat_id, 'Введите длину пароля')

    elif type(msg) == int:
        send(chat_id, new_password(msg))

    else:
        send(chat_id, 'Я тебя не понимаю 😐')


bot.polling(none_stop=True)
