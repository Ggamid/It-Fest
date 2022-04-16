import telebot
import requests
import vk_api
from telebot import types
import time
from requests import get
from Sqlighter import Sqlighter
from threading import Thread
from datetime import date
import datetime

token = "5248705269:AAF0vUzDRuf3nYV-M6Ur9OFnlQNyx_izGKY"
tokenVK = "fd98b0c9fd98b0c9fd98b0c984fde4b800ffd98fd98b0c99fd5c972905042d874946aa7"
version = 5.131
domain = "nauchim.online"
session = vk_api.VkApi(token=tokenVK)
vk = session.get_api()

current_data = str(date.today())[5:]
bot = telebot.TeleBot(token)
list_stiker = open("AnimatedStickerList.tgs", "rb")

dict_perfom = {1: ['Международный конкурс детских инженерных команд', '#TechnoCom'],
               2: ['Международный фестиваль информационных технологий «ITфест»', '#IT-fest_2022'],
               3: ['Всероссийский фестиваль общекультурных компетенций', '#ФестивальОКК'],
               4: ['Всероссийский фестиваль нейротехнологий «Нейрофест»', '#Нейрофест'],
               5: ['Всероссийский конкурс по микробиологии «Невидимый мир»', '#НевидимыйМир'],
               6: ['Всероссийский конкурс научноисследовательски работ', '#КонкурсНИР'],
               7: ['Международный аэрокосмический фестиваль', '#IASF2022'],
               8: ['Международный фестиваль 3Dмоделирования и программирования VRAR-Fest', '#VRARFest3D']}

stroka = ""
for i in range(1, len(dict_perfom)):
    stroka += dict_perfom[i][0] + " " + dict_perfom[i][1] + "\n"

identificator = 0


# Bot begin
@bot.message_handler(commands=['start', 'add_tag', 'remove_tag', 'change_sending'])
def start_message(message):
    global identificator
    identificator = message.from_user.id

    if message.text == "/start":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        support = types.KeyboardButton("Поддержка⚙️")  # добавление клавиатуры
        add_tag = types.KeyboardButton("/add_tag")
        remove_tag = types.KeyboardButton("/remove_tag")
        on_off = types.KeyboardButton("/change_sending")

        markup.add(support, add_tag, remove_tag, on_off)

        send_mess = f"Салам {message.from_user.first_name}"
        sti = open("AnimatedSticker.tgs", "rb")
        bot.send_sticker(message.chat.id, sti)  # отправка стикера
        bot.send_message(message.chat.id,
                         f'{send_mess}!, Я бот🤖, Меня зовут YaNotifi! и моя цель уведомлять тебя '
                         f'о новых постах в сообществе вконтакте под названием '
                         f'Научим Online❕📨'.format(message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=markup)

        bot.send_message(message.chat.id, "Пользуйся командами 🔧 в клавиатуре опишу их:  "
                                          "\n /change_sending - с помощью нее ты можешь отключать и включать отправку уведомлений"
                                          "\n /add_tag - с помощью этой команды можешь добавлять желаемые хэштэги и бот будет уведомлять о записях с таким хэштэгом "
                                          "\n /remove_tag - благодаря ей удаляй больше не интересующие хэштэги")

        Sqlighter.add_id(message.from_user.id)




    elif message.text == "/add_tag":

        bot.send_message(message.chat.id, f"Ваш нынешний список: \n{Sqlighter.get_tag(message.from_user.id)}")
        bot.send_message(message.chat.id, f"Доступные хэштэги: \n{stroka} \n Как много мероприятий, неправда ли? Думаю каждый найдет то, что ему по душе!😁")
        bot.send_message(message.chat.id, "Отправь хэштэг на который хотите подписаться в формате 📥:")
        bot.send_message(message.chat.id, "YaNotifi, Добавь хэштэг: #text")


    elif message.text == "/remove_tag":
        bot.send_sticker(message.chat.id, list_stiker)
        bot.send_message(message.chat.id, f"Ваш нынешний список: \n{Sqlighter.get_tag(message.from_user.id)}")
        bot.send_message(message.chat.id, "Отправь хэштэг от которого хотите отписаться  🚮 в формате:".format())
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
            bot.send_message(message.chat.id, "Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты: "
                                              "\n Группа ВКонтакте Научим.online https://vk.com/nauchim.online "
                                              "\n Сайт с мероприятиями https://www.научим.online")
        elif "YaNotifi, Добавь хэштэг:" in message.text:
            ls = []
            Sqlighter.add_tag_to_id(identificator, find_teg_in_stroke(message.text, ls)[0])

        elif "YaNotifi, Удали хэштэг:" in message.text:
            ls = []
            Sqlighter.remove_tag_from_id(identificator, find_teg_in_stroke(message.text, ls)[0])

        else:
            bot.send_message(message.chat.id,
                             "Я тебя не понимаю 🤖.Используй мои команды!:"
                             " \n         /add_tag - добавить хэштэг "
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
                # show alert
                if Sqlighter.change_sendind(identificator, 1) == "ИЗМЕНЕНИЯ СОХРАНЕНЫ":
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text="Отправка уведомлений продолжится😌")
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text="Что-то пошло не так🤔, напишите в поддержку")
            elif call.data == 'StopSending':
                Sqlighter.change_sendind(identificator, 0)
                # show alert
                if Sqlighter.change_sendind(identificator, 0) == "ИЗМЕНЕНИЯ СОХРАНЕНЫ":
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text="Отправка уведомлений остановлена😌")

                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text="Что-то пошло не так🤔, напишите в поддержку")

    except Exception as e:
        print(repr(e))


def sender():
    try:
        list_user = Sqlighter.get_id_list()
        list_post = GetInfo(domain)

        while True:
            for i in list_user:
                list_tag = Sqlighter.get_tag(i)
                for tag in list_tag:
                    for post in list_post:
                        if tag in list_post[post][1] and list_post[post][0] and Sqlighter.check_post_in_sent_post(i, list_post[post][4]) == "Можно Отправить" and list_post[post][3]:
                            bot.send_message(i, list_post[post][1])
                            Sqlighter.add_id_post_to_sent_post(i, list_post[post][4])
            time.sleep(1800)
    except TypeError as e:
        sender()
        print("Error", e)

#
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
        text_data = float(data2[i]["date"])
        id_post = str(data2[i]["id"])
        img_post = None
        check_data = False

        value = datetime.datetime.fromtimestamp(text_data)
        date_post = value.strftime('%m-%d')

        if "attachments" in data2[i]:
            if data2[i]["attachments"][0]["type"] == "photo":
                img_post = data2[i]['attachments'][0]["photo"]["sizes"][4]["url"]

        if current_data == date_post:
            check_data = True

        list_post_text[i] = [date_post, text_post, img_post, check_data, id_post]

    return list_post_text


def GetText(
        domain):  # эта функция нужна чтобы сделать список только из постов, чтобы потом этот список передать в функцию find_tag И она найдет все тэги из 40 публикаций
    data = pars(domain)  # Неструктурированные данные

    data2 = data["items"]
    list_post_text = []

    for i in range(0, len(data2)):  # вытаскиваем из data2 тексты постов
        text_post = data2[i]["text"]
        list_post_text.append(text_post)

    return list_post_text


def send_post_Htag(text_hashtag, dict_info, id):  # функция проходится по словарю и ищет публикации с нужными хэштэгами
    for i in range(0, len(dict_info)):
        print(dict_info([i][1]))
        if text_hashtag in dict_info[i][1] and dict_info[i][3] and (
                Sqlighter.check_post_in_sent_post(id, dict_info[i][4]) == "Можно Отправить"):

            list_for_send = [dict_info[i][1], dict_info[i][4]]

        else:
            list_for_send = ["такого тэга нет", ""]
    return list_for_send


def find_teg(text, teg_list):
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


def find_teg_in_stroke(text, teg_list):
    index = 0
    for i in range(text.index('#'), len(text)):
        if text[i] == ' ' or i == (len(text) - 1):
            teg_list.append(text[text.index('#'):i + 1])
            index = i
            break
    if text.count('#') > 1:  # sender()
        find_teg_in_stroke(text[index:len(text)], teg_list)
    return teg_list


t2 = Thread(target=bot.polling(none_stop=True))
t2.start()
