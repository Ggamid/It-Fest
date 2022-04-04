
import telebot
import requests
from telebot import types

token = "5248705269:AAF0vUzDRuf3nYV-M6Ur9OFnlQNyx_izGKY"

bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):

  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

  support = types.KeyboardButton("Поддержка⚙️")


  markup.add(support)
  send_mess = f"Hello {message.from_user.first_name}"
  bot.send_message(message.chat.id,
                   f'Салам {message.from_user.first_name}!, Я бот🤖, новостной бот, на данный момент я умею отправлять новости📰, выбери из предложенных тем, интересную тебе❕⬇️'.format(
                     message.from_user, bot.get_me()),
                   parse_mode='html', reply_markup=markup)


bot.polling(none_stop=True)