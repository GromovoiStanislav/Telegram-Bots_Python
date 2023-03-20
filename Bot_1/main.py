import telebot
import os

from telebot import types
from dotenv import dotenv_values, load_dotenv

# config = dotenv_values(".env")
# bot = telebot.TeleBot(config['TELEGRAM_TOKEN'])

load_dotenv()
bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # bot.reply_to(message, "Howdy, how are you doing?")
    mess = f'Привет <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Посетить веб-сайт', url="https://pypi.org/project/pyTelegramBotAPI/"))
    bot.send_message(message.chat.id, 'Перейдите на сайт', reply_markup=markup)


@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    website = types.KeyboardButton('/website')
    start = types.KeyboardButton('/start')
    btn = types.KeyboardButton('Контакты')
    markup.add(website, start, btn)
    bot.send_message(message.chat.id, 'Привет!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Hello':
        bot.send_message(message.chat.id, 'И тебе привет!')
    elif message.text == 'ID':
        bot.send_message(message.chat.id, f'Твой ID: {message.from_user.id}')
    elif message.text == 'Контакты':
        bot.send_message(message.chat.id, 'Выслал контакты на твой email')
    elif message.text == 'photo':
        photo = open('biscuit.webp', 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text == 'sticker':
        sticker = open('biscuit.webp', 'rb')
        bot.send_sticker(message.chat.id, sticker)
    elif message.text == 'Location':
        bot.send_location(message.chat.id, 42.816207, 74.6243105)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю '+message.text)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Вау...')


bot.polling(none_stop=True)
