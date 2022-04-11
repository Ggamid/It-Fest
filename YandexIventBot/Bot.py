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


# Bot begin
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    support = types.KeyboardButton("Поддержка⚙️") #добавление клавиатуры

    markup.add(support)
    send_mess = f"Hello {message.from_user.first_name}"
    sti = open("AnimatedSticker.tgs", "rb")

    bot.send_sticker(message.chat.id, sti) # отправка стикера
    bot.send_message(message.chat.id,
                     f'Салам {message.from_user.first_name}!, Я бот🤖, Меня зовут YaNotifi! Я буду уведомлять тебя о новых постах в сообществе вконтакте под названием Научим Online❕'.format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id,
                     'Отправь мне хэштэг # и я вышлю тебе последние публикации с ним'.format())



@bot.message_handler(content_types=['text', "sticker"])
def lalala(message):
    text_hashtag = message.text #получени текста сообщения
    dict_info = GetInfo(domain) #словарь с публикациями
    bot.send_message(message.chat.id, send_post_Htag(text_hashtag, dict_info))


# Bot_end


def pars(domain):
    status = session.method("wall.get", {"domain": domain, "count": 10})  #запрос в vk api
    return status


def GetInfo(domain):
    data = pars(domain)  # Неструктурированные данные

    data2 = data["items"]
    list_post_text = {}

    for i in range(0, len(data2)):  # вытаскиваем из data2 тексты постов
        text_post = data2[i]["text"]
        text_data = data2[i]["date"]
        img_post = None
        if "attachments" in data2[i]:
            if data2[i]["attachments"][0]["type"] == "photo":
                img_post = data2[i]['attachments'][0]["photo"]["sizes"][4]["url"]
        list_post_text[i] = [text_data, text_post, img_post]


    return list_post_text


def send_post_Htag(text_hashtag, dict_info): # функция проходится по словарю и ищет публикации с нужными хэштэгами
    for i in range(0, 10):
        if text_hashtag in dict_info[i][1]:
            stroka_for_send = dict_info[i][1] + "\n" + dict_info[i][2]
            break
    else:
        stroka_for_send = "такого тэга нет"
    return stroka_for_send



bot.polling(none_stop=True)