import sqlite3

connect = sqlite3.connect('db_id_tag.db')  # подключаемся к БД
cursor = connect.cursor()

table = """
CREATE TABLE IF NOT EXISTS user(
    id BIGINT,
    tag TEXT,
    status INTEGER(1) DEFAULT 0,
    sent_post TEXT
);
"""
cursor.execute(table)


class Sqlighter:

    def check_user(id):  # проверяет есть ли пользователь в БД
        try:
            connect = sqlite3.connect("db_id_tag.db")
            cursor = connect.cursor()

            cursor.execute("SELECT id FROM user WHERE id =?", [id])
            if cursor.fetchone() is None:
                return "ТАКОГО ID НЕТ"
            else:
                return True
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()

    def add_id(id):  # дабавляет пользователя в БД
        try:

            connect = sqlite3.connect('db_id_tag.db')  # подключаемся к БД
            cursor = connect.cursor()  # подключаем способность редактирования

            cursor.execute("SELECT id FROM user WHERE id = ?", [id])  # получаем значение
            if cursor.fetchone() is None:  # проверяем есть ли у нас такой id или нет

                cursor.execute("INSERT INTO user(id) VALUES(?);", [id])  # если нет, то добавляем
                connect.commit()  # подтверждаем изменения
                return "ПОЛЬЗОВАТЕЛЬ УСПЕШНО ДОБАВЛЕН"
            else:  # если есть отправлем сообщение
                return "ТАКОЙ ПОЛЬЗОВАТЕЛЬ УЖЕ СУЩЕСТВУЕТ"


        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()  # после обработки метода отключаем способность редактирования
            connect.close()  # отключаемся от БД

    def add_tag_to_id(id, tag):  # добавляет тэг к пользователю
        try:

            connect = sqlite3.connect('db_id_tag.db')  # подключаемся к БД
            cursor = connect.cursor()  # подключаем способность редактирования

            cursor.execute("SELECT id FROM user WHERE id = ?", [id])
            if cursor.fetchone() is None:  # проверяем есть ли у нас такой id или нет
                return "ID НЕ НАЙДЕНО"
            else:  # если есть то добавляем хэштэги
                new_tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[
                    0]  # берем существующие тэги
                print(new_tag)
                if new_tag is None or new_tag == "":  # если тэгов нет то просто ставим переданный тэг
                    new_tag = tag
                elif tag not in new_tag:  # если тэги есть то к существующим добавляем новый
                    new_tag = new_tag + "," + tag

                cursor.execute("UPDATE user SET tag = ? WHERE id = ?",
                               [new_tag, id])  # добавляем в столбец tag значение переменной new_tag
                cursor.execute("UPDATE user SET status = ? WHERE id = ?", [1, id])  # подключаем человека к рассылке
                connect.commit()  # подтверждаем изменения
                return "TAG ДОБАВЛЕН"

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()  # после обработки метода отключаем способность редактирования
            connect.close()  # отключаемся от БД

    def change_sendind(id, status):  # изменение статуса отправки сообщений
        try:
            connect = sqlite3.connect("db_id_tag.db")  # подключаемся к БД
            cursor = connect.cursor()  # подключаем способность редактирования

            cursor.execute("SELECT id FROM user WHERE id = ?", [id])
            if cursor.fetchone() is None:
                return "ТАКОГО ID НЕТ"
            else:
                cursor.execute("UPDATE user SET status = ? WHERE id = ?", [status, id])
                connect.commit()  # подтверждаем изменения
                return "ИЗМЕНЕНИЯ СОХРАНЕНЫ"

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()  # после обработки метода отключаем способность редактирования
            connect.close()  # отключаемся от БД

    def remove_tag_from_id(id, tag):  # удаляет у определенного пользователя
        try:

            connect = sqlite3.connect("db_id_tag.db")  # подключаемся к БД
            cursor = connect.cursor()  # подключаем способность редактирования

            if Sqlighter.check_user(id):
                prom = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0]
                if prom is not None and prom != "":
                    old_tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0].split(
                        ",")  # вытаскиваем строку с тэгами и превращаем ее в список с тэгами
                    if tag in old_tag:
                        old_tag.remove(tag)  # удаляем ненужный тэг
                        new_tag = ",".join(old_tag)  # cоздаем новую строку которую будем добавлять в бд
                        cursor.execute("UPDATE user SET tag = ? WHERE id = ?",
                                       [new_tag, id])  # дабавляем отредактированные тэги
                        connect.commit()  # подтверждаем изменения
                        return 'СПИСОК ХЭШТЭГОВ ИЗМЕНЕН'
                    else:
                        return "Такого тэга нет в списке"
                return "У пользователя нет тэгов"
            return "Такого пользователя нет"




        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()  # после обработки метода отключаем способность редактирования
            connect.close()  # отключаемся от БД

    def check_out_status(id):  # проверка на то, нужно ли отправлять пользователю уведомления или нет
        try:
            connect = sqlite3.connect("db_id_tag.db")  # подключаемся к БД
            cursor = connect.cursor()  # подключаем способность редактирования

            tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0]
            status = cursor.execute("SELECT status FROM user WHERE id = ?", [id]).fetchone()[0]

            if tag is None or tag == "" or status == 0:  # если в тэге ничего нет или тэг это пустая строчка или статус равен 0 то пользоваетель не подходит под рассылку, иначе - подходит
                return False
            else:
                return True
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()

    def get_tag(id):  # проверяем есть ли в поле tag у пользователя хэштэги, если есть возвращаем их
        try:

            connect = sqlite3.connect("db_id_tag.db")
            cursor = connect.cursor()

            if Sqlighter.check_user(id) != True:
                return "ТАКОГО ID НЕТ"
            else:
                tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0]
                if tag is None or tag == "":
                    return "Вы еще не подписаны на хэштэги"
                else:
                    return tag
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()

    def get_id_list():  # получаем из базы данных сисок с id пользователей которым будем отправлять уведомления
        try:
            connect = sqlite3.connect("db_id_tag.db")
            cursor = connect.cursor()
            a = cursor.execute(
                "SELECT id FROM user WHERE status = 1").fetchall()  # берем айди пользователей у которых статус равен 1 то есть который готов получать увдеомления
            newlst = []
            for i in a:
                for x in i:
                    newlst.append(x)
            return newlst
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()

    def add_id_post_to_sent_post(id_user,
                                 id_post):  # добавлем в бд к пользователю Id post идентификатор поста который отправили
        try:
            id_post = str(id_post)
            connect = sqlite3.connect("db_id_tag.db")
            cursor = connect.cursor()

            new_post_id = str(cursor.execute("SELECT sent_post FROM user WHERE id = ?", [id_user]).fetchone()[
                                  0])  # берем id тех публикаций которые уже были отправлены

            if new_post_id is None or new_post_id == "":
                new_post_id = id_post
            else:
                new_post_id = new_post_id + "," + id_post

            if Sqlighter.check_user(id_user):
                cursor.execute("UPDATE user SET sent_post = ? WHERE id = ?",
                               [new_post_id, id_user])  # и добавляем к ним новый
                connect.commit()

                return "done"
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()

    def check_post_in_sent_post(id, id_post):  # проверка на то отправляли ли мы этот пост или нет
        try:
            connect = sqlite3.connect("db_id_tag.db")
            cursor = connect.cursor()

            if Sqlighter.check_user(id):
                stroka_with_post_id = cursor.execute("SELECT sent_post FROM user WHERE id = ?", [id]).fetchone()[
                    0]  # берем посты которые отправлены пользователю
                if stroka_with_post_id is None:
                    return "Не отправлять"
                else:
                    stroka_with_post_id.split(",")
                    if str(id_post) in stroka_with_post_id:  # проверяем был ли пост отправлен пользователю ранее
                        return "Не отправлять"
                    else:
                        return "Можно Отправить"

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()
