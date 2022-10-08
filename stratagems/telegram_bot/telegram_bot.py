import telebot
import os
import requests
from telebot import types

bot = telebot.TeleBot("5590703280:AAFBbiTwGWII0Dpw0jtOSRgSRyanTzr8cps")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    hideBoard = types.ReplyKeyboardRemove()
    select_category = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton("Бухгалтер 🧮")
    itembtn2 = types.KeyboardButton("Генеральный директор 🏢")
    select_category.add(itembtn1, itembtn2)

    if message.text is None:
        bot.send_message(message.from_user.id,
                         '''Я тебя не совсем понимаю, напиши /start''',
                         parse_mode="HTML",
                         reply_markup=hideBoard)
    elif message.text == 'Бухгалтер 🧮':
        r = requests.get('http://127.0.0.1:8000/news/buh/').json()
        bot.send_message(message.from_user.id,
                         f'<b>Новости по запросу "бухгалтер"</b>\n\n🧮<b>{r[0]["title"]}</b>\n{r[0]["text"]}\n\n🧮<b>{r[1]["title"]}</b>\n{r[1]["text"]}\n\n🧮<b>{r[2]["title"]}</b>\n{r[2]["text"]}',
                         parse_mode="HTML",
                         reply_markup=select_category)
    elif message.text == 'Генеральный директор 🏢':
        r = requests.get('http://127.0.0.1:8000/news/director/').json()
        bot.send_message(message.from_user.id,
                         f'<b>Новости по запросу "генеральный директор"</b>\n\n🏢<b>{r[0]["title"]}</b>\n{r[0]["text"]}\n\n🏢<b>{r[1]["title"]}</b>\n{r[1]["text"]}\n\n🏢<b>{r[2]["title"]}</b>\n{r[2]["text"]}',
                         parse_mode="HTML",
                         reply_markup=select_category)
    elif message.text.lower() == '/start' or message.text.lower() == '/help':
        bot.send_message(
            message.from_user.id,
            '''Приветствую, выбери категорию, по которой прислать самые актуальные новости.''',
                         parse_mode="HTML", reply_markup=select_category)

    else:
        bot.send_message(message.from_user.id,
                         '''Я тебя не совсем понимаю, напиши /start''',
                         parse_mode="HTML",
                         reply_markup=hideBoard)

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
