import sqlite3


connect = sqlite3.connect('db_id_tag.db')   # подключаемся к БД
cursor = connect.cursor()



table = """
CREATE TABLE IF NOT EXISTS user(
    id INTEGER,
    tag TEXT,
    status INTEGER(1) DEFAULT 0
);
"""
cursor.execute(table)

class Sqlighter:



    def add_id(id):
        try:

            connect = sqlite3.connect('db_id_tag.db')  # подключаемся к БД
            cursor = connect.cursor()   # подключаем способность редактирования

            cursor.execute("SELECT id FROM user WHERE id = ?", [id]) # получаем значение
            if cursor.fetchone() is None: # проверяем есть ли у нас такой id или нет

                cursor.execute("INSERT INTO user(id) VALUES(?);", [id]) # если нет, то добавляем
                connect.commit() # подтверждаем изменения
                return "ПОЛЬЗОВАТЕЛЬ УСПЕШНО ДОБАВЛЕН"
            else: # если есть отправлем сообщение
                return "ТАКОЙ ПОЛЬЗОВАТЕЛЬ УЖЕ СУЩЕСТВУЕТ"


        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close() # после обработки метода отключаем способность редактирования
            connect.close() # отключаемся от БД


    def add_tag_to_id(id, tag):
        try:

            connect = sqlite3.connect('db_id_tag.db')  # подключаемся к БД
            cursor = connect.cursor()   # подключаем способность редактирования

            cursor.execute("SELECT id FROM user WHERE id = ?", [id])
            if cursor.fetchone() is None: # проверяем есть ли у нас такой id или нет
                return "ID НЕ НАЙДЕНО"
            else: #  если есть то добавляем хэштэги
                new_tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0] # берем существующие тэги
                print(new_tag)
                if new_tag is None or new_tag == "":# если тэгов нет то просто ставим переданный тэг
                    new_tag = tag
                elif tag not in new_tag: # если тэги есть то к существующим добавляем новый
                    new_tag = new_tag + "," + tag

                cursor.execute("UPDATE user SET tag = ? WHERE id = ?", [new_tag, id]) # добавляем в столбец tag значение переменной new_tag
                cursor.execute("UPDATE user SET status = ? WHERE id = ?", [1, id]) # подключаем человека к рассылке
                connect.commit() # подтверждаем изменения
                return "TAG ДОБАВЛЕН"

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()# после обработки метода отключаем способность редактирования
            connect.close() # отключаемся от БД

    def change_sendind(id, status): # изменение статуса отправки сообщений
        try:
            connect = sqlite3.connect("db_id_tag.db")  # подключаемся к БД
            cursor = connect.cursor() # подключаем способность редактирования

            cursor.execute("SELECT id FROM user WHERE id = ?", [id])
            if cursor.fetchone() is None:
                return "ТАКОГО ID НЕТ"
            else:
                cursor.execute("UPDATE user SET status = ? WHERE id = ?", [status, id])
                connect.commit() # подтверждаем изменения
                return "ИЗМЕНЕНИЯ СОХРАНЕНЫ"

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()# после обработки метода отключаем способность редактирования
            connect.close() # отключаемся от БД


    def remove_tag_from_id(id, tag):
        try:

            connect = sqlite3.connect("db_id_tag.db")  # подключаемся к БД
            cursor = connect.cursor()   # подключаем способность редактирования

            a = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0]  #Проверка есть ли в базе данное ID
            b = cursor.execute("SELECT id FROM user WHERE id = ?", [id])
            if a is None or a == "" or "#" not in a or b is None:
                return "ID НЕТ В БАЗЕ ИЛИ В TAG НИЧЕГО НЕТ"
            elif tag in cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0].split(","):
                print("good")
                old_tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0].split(",")  #вытаскиваем строку с тэгами и превращаем ее в список с тэгами
                old_tag.remove(tag)  #удаляем ненужный тэг
                new_tag = ",".join(old_tag)  #cоздаем новую строку которую будем добавлять в бд
                cursor.execute("UPDATE user SET tag = ? WHERE id = ?", [new_tag, id])  #дабавляем отредактированные тэги
                connect.commit() # подтверждаем изменения
                return 'СПИСОК ХЭШТЭГОВ ИЗМЕНЕН'

            # new_tag = ",".join(old_tag)

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()# после обработки метода отключаем способность редактирования
            connect.close() # отключаемся от БД



    def check_out_status(id): # проверка на то, нужно ли отправлять пользователю уведомления или нет
        try:
            connect = sqlite3.connect("db_id_tag.db")  # подключаемся к БД
            cursor = connect.cursor()  # подключаем способность редактирования

            tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0]
            status = cursor.execute("SELECT status FROM user WHERE id = ?", [id]).fetchone()[0]

            if tag is None or tag == "" or status == 0: #если в тэге ничего нет или тэг это пустая строчка или статус равен 0 то пользоваетель не подходит под рассылку, иначе - подходит
                return False
            else:
                return True
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()



    def get_tag(id):
        try:

            connect = sqlite3.connect("db_id_tag.db")
            cursor = connect.cursor()
            cursor.execute("SELECT id FROM user WHERE id =?", [id])
            if cursor.fetchone() is None:
                return "ТАКОГО ID НЕТ"
            else:
                tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0]
                if tag is None:
                    return "Вы еще не подписаны на хэштэги"
                else:
                    return tag
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()





