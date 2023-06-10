import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(types.KeyboardButton('Отправить картинку'), types.KeyboardButton('Отправить файл'))
    keyboard.add(types.KeyboardButton('Ответить на вопрос'))
    bot.send_message(chat_id=message.chat.id, text=f'Привет {message.from_user.first_name}!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if message.text == 'Отправить картинку':
        # photo = open('cat.webp', 'rb')
        photo = 'https://cdnn21.img.ria.ru/images/144814/13/1448141397_0:219:4256:2613_600x0_80_0_0_63288125b270a45f0d94b82b7a172fcf.jpg.webp'
        bot.send_photo(chat_id=message.chat.id, photo=photo, caption='Это кошка')

    elif message.text == 'Отправить файл':
        file = open('requirements.txt', 'rb')
        bot.send_document(chat_id=message.chat.id, document=file, caption='Очень важный файл')

    elif message.text == 'Ответить на вопрос':
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(types.InlineKeyboardButton('2', callback_data='2'),
                     types.InlineKeyboardButton('4', callback_data='4'),
                     types.InlineKeyboardButton('5', callback_data='5'))
        bot.send_message(chat_id=message.chat.id, text='2 + 2 = ?', reply_markup=keyboard)

    else:
        bot.send_message(chat_id=message.chat.id, text='Я тебя не понимаю')


@bot.callback_query_handler(func=lambda call: True)
def getAnswer(call):
    if call.data == '4':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Верно!')
    else:
        bot.send_message(chat_id=call.message.chat.id, text='Ответ не верный, попробуйте снова')
    bot.answer_callback_query(call.id)  # чтобы убрать часики с кнопок


bot.polling(none_stop=True)
