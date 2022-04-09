
import telebot
import requests
import vk_api
from telebot import types

token = "5248705269:AAF0vUzDRuf3nYV-M6Ur9OFnlQNyx_izGKY"
tokenVK = "fd98b0c9fd98b0c9fd98b0c984fde4b800ffd98fd98b0c99fd5c972905042d874946aa7"
version = 5.131
domain = "nauchim.online"
session = vk_api.VkApi(token=tokenVK)
vk = session.get_api()

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



def pars(domain):
    status = session.method("wall.get", {"domain":domain, "count":10})
    return status

def GetInfo(domain):
    data = pars(domain)

    data2 = data["items"]
    list_post_text = {}
    # print(data2)

    for i in range(0, len(data2)): # вытаскиваем из data2 тексты постов
        text_post = data2[i]["text"]
        text_data = data2[i]["date"]
        list_post_text[text_data] = text_post



    return list_post_text




    # print(data2[2]["text"])


# bot.polling(none_stop=True)