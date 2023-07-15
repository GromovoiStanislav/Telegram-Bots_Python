from bs4 import BeautifulSoup
import requests
import random
import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()


def get_jokes():
    url = 'https://www.anekdot.ru/last/anekdot/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    jokes = soup.findAll('div', class_='text')
    return [j.text for j in jokes]


list_of_jokes = get_jokes()
random.shuffle(list_of_jokes)


bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton('Продолжить...', callback_data='get_joke'))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text='Привет! У меня есть парочка свежих анекдотов для тебя',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def get_joke(call):
    if call.data == 'get_joke':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=call.message.text)
        # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        if len(list_of_jokes) > 0:
            bot.send_message(chat_id=call.message.chat.id, text=list_of_jokes[0], reply_markup=keyboard)
            del list_of_jokes[0]
        else:
            bot.send_message(chat_id=call.message.chat.id, text='Опс... На сегодня все анекдоты закончились 😳')
    bot.answer_callback_query(call.id)  # чтобы убрать часики с кнопок


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(chat_id=message.chat.id, text='Я тебя не понимаю 😐')





bot.polling(none_stop=True)