import telebot
import os
from telebot import types

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    hideBoard = types.ReplyKeyboardRemove()

    if message.text is None:
        bot.send_message(message.from_user.id,
                         '''Я тебя не совсем понимаю, напиши /start''',
                         parse_mode="HTML",
                         reply_markup=hideBoard)
    elif message.text == 'Я — бухгалтер 🧮':
        bot.send_message(message.from_user.id,
                         f'Рады знакомству, бухгалтер, {message.from_user.first_name}. Теперь мы будем отправлять новости из вашего круга интересов.',
                         parse_mode="HTML",
                         reply_markup=hideBoard)
    elif message.text == 'Я — генеральный директор 🏢':
        bot.send_message(message.from_user.id,
                         f'Рады знакомству, генеральный директор, {message.from_user.first_name}. Теперь мы будем отправлять новости из вашего круга интересов.',
                         parse_mode="HTML",
                         reply_markup=hideBoard)
    elif message.text.lower() == '/help':
        bot.send_message(message.from_user.id,
                         '''Привет, я новостной бот втб. Вот мои основные функции: ''',
                         parse_mode="HTML",
                         reply_markup=hideBoard)
    elif message.text.lower() == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn1 = types.KeyboardButton("Я — бухгалтер 🧮")
        itembtn2 = types.KeyboardButton("Я — генеральный директор 🏢")
        markup.add(itembtn1, itembtn2)
        bot.send_message(
            message.from_user.id,
            '''Добрый день. Давайте познакомимся, расскажите, чем вы занимаетесь? ''',
                         parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(message.from_user.id,
                         '''Я тебя не совсем понимаю, напиши /start''',
                         parse_mode="HTML",
                         reply_markup=hideBoard)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
