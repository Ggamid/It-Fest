import telebot
import requests
import vk_api
from telebot import types
import time
from requests import get
from Sqlighter import Sqlighter
from threading import Thread

token = "5248705269:AAF0vUzDRuf3nYV-M6Ur9OFnlQNyx_izGKY"
tokenVK = "fd98b0c9fd98b0c9fd98b0c984fde4b800ffd98fd98b0c99fd5c972905042d874946aa7"
version = 5.131
domain = "nauchim.online"
session = vk_api.VkApi(token=tokenVK)
vk = session.get_api()

bot = telebot.TeleBot(token)

identificator = 0
# Bot begin
@bot.message_handler(commands=['start', 'add_tag', 'remove_tag', 'change_sending'])
def start_message(message):

    global identificator
    identificator = message.from_user.id

    if message.text == "/start":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        support = types.KeyboardButton("Поддержка⚙️")  # добавление клавиатуры

        markup.add(support)
        send_mess = f"Hello {message.from_user.first_name}"
        sti = open("AnimatedSticker.tgs", "rb")
        bot.send_sticker(message.chat.id, sti)  # отправка стикера
        bot.send_message(message.chat.id,
                         f'Салам {message.from_user.first_name}!, Я бот🤖, Меня зовут YaNotifi! и моя цель уведомлять тебя '
                         f'о новых постах в сообществе вконтакте под названием '
                         f'Научим Online❕📨'.format(message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=markup)
        Sqlighter.add_id(message.from_user.id)

    elif message.text == "/add_tag":

        empti = []
        empti = set(find_teg(GetText(domain), empti))
        bot.send_message(message.chat.id, f"Ваш нынешний список: \n{Sqlighter.get_tag(message.from_user.id)}")
        bot.send_message(message.chat.id, "Хэштэги из последних 40ка публикаций: \n{}".format(empti))
        bot.send_message(message.chat.id, "Отправь хэштэг на который хотите подписаться в формате 📥:")
        bot.send_message(message.chat.id, "YaNotifi, Добавь хэштэг: #text")


    elif message.text == "/remove_tag":

        bot.send_message(message.chat.id, f"Ваш нынешний список: \n{Sqlighter.get_tag(message.from_user.id)}")
        bot.send_message(message.chat.id, "Отправь хэштэг от которого хотите отписаться в формате 🚮:".format())
        bot.send_message(message.chat.id, "YaNotifi, Удали хэштэг: #text".format())



    elif message.text == "/change_sending":

        markup = types.InlineKeyboardMarkup(row_width=1)
        item_change_1 = types.InlineKeyboardButton("Остановить⛔️", callback_data="StopSending")
        item_change_2 = types.InlineKeyboardButton("Продолжить📫", callback_data="ContinueSending")
        markup.add(item_change_1, item_change_2)

        bot.send_message(message.chat.id,
                         "Хотите Остановить отправку сообщений? - нажмите Остановить "
                         "\n Хотите Продолжить отправку сообщений? - нажмите Продолжить",
                         reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == "private":
        if message.text == "Поддержка⚙️":
            bot.send_message(message.chat.id, "@GGAMID")
        else:
            bot.send_message(message.chat.id,
                             "Используй мои команды: \n         /add_tag - добавить хэштэг "
                             "\n         /change_sending - отключение\включение рассылки "
                             "\n         /remove_tag - отписаться от определенного хэштэга")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        global identificator
        if call.message:
            # news
            if call.data == 'ContinueSending':
                Sqlighter.change_sendind(identificator, 1)
                print(identificator)
                # show alert
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                    text=Sqlighter.change_sendind(identificator, 1))
            elif call.data == 'StopSending':
                Sqlighter.change_sendind(identificator, 0)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                    text=Sqlighter.change_sendind(identificator, 0))
    except Exception as e:
        print(repr(e))


def sender():
    list_user = Sqlighter.get_id_list(identificator)
    list_post = GetInfo(domain)

    while True:
        for i in list_user:
            list_tag = Sqlighter.get_tag(i)
            sended_tag = []
            for tag in list_tag:

                if send_post_Htag(tag, list_post) != "такого тэга нет" and tag not in sended_tag:
                    bot.send_message(i, send_post_Htag(tag, list_post))
                    sended_tag.append(tag)
        time.sleep(100000)


t1 = Thread(target=sender)
t1.start()
# Bot_end


def pars(domain):
    status = session.method("wall.get", {"domain": domain, "count": 50})  # запрос в vk api
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


def GetText(domain):   # эта функция нужна чтобы сделать список только из постов, чтобы потом этот список передать в функцию find_tag И она найдет все тэги из 40 публикаций
    data = pars(domain)  # Неструктурированные данные

    data2 = data["items"]
    list_post_text = []

    for i in range(0, len(data2)):  # вытаскиваем из data2 тексты постов
        text_post = data2[i]["text"]
        list_post_text.append(text_post)

    return list_post_text


def send_post_Htag(text_hashtag, dict_info):  # функция проходится по словарю и ищет публикации с нужными хэштэгами
    for i in range(0, len(dict_info)):
        if text_hashtag[0] == "#" and text_hashtag in dict_info[i][1]:
            stroka_for_send = dict_info[i][1]
            break
        else:
            stroka_for_send = "такого тэга нет"
    return stroka_for_send


def find_teg(list, teg_list):
    index = 0
    for item in list:
        if "#" in item:
            for i in range(item.index('#'), len(item)):
                if item[i] == ' ' or i == (len(item) - 1):
                    teg_list.append(item[item.index('#'):i + 1])
                    index = i
                    break
        if item.count('#') > 1:
            find_teg(item[index:len(item)], teg_list)
    return teg_list


# bot.polling(none_stop=True)
t2 = Thread(target=bot.polling(none_stop=True))
t2.start()
