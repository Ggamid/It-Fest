import sqlite3


connect = sqlite3.connect('db_id_tag.db')
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
            cursor.execute("SELECT id FROM user WHERE id = ?", [id])
            if cursor.fetchone() is None:

                cursor.execute("INSERT INTO user(id) VALUES(?);", [id])
                connect.commit()

            else:
                print("Такой id уже существует")

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()


    def add_tag_to_id(tag, id):
        try:

            connect = sqlite3.connect('db_id_tag.db')
            cursor = connect.cursor()

            cursor.execute("SELECT id FROM user WHERE id = ?", [id])
            if cursor.fetchone() is None:
                print("Нет такого id")
            else:
                new_tag = cursor.execute("SELECT tag FROM user WHERE id = ?", [id]).fetchone()[0]
                if new_tag is None:
                    new_tag = tag
                else:
                    new_tag = new_tag + "," + tag
                print(new_tag)
                cursor.execute("UPDATE user SET tag = ? WHERE id = ?", [new_tag, id])
                cursor.execute("UPDATE user SET status = ? WHERE id = ?", [1, id])
                connect.commit()

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()

    def turn_off_sendind(id):
        try:
            connect = sqlite3.connect("db_id_tag.db")
            cursor = connect.cursor()

            cursor.execute("SELECT id FROM user WHERE id = ?", [id])
            if cursor.fetchone() is None:
                print("Нет такого id")
            else:
                cursor.execute("UPDATE user SET status = ? WHERE id = ?", [0, id])
                connect.commit()
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            connect.close()



    def remove_tag_from_id(id, tag):

        pass
Sqlighter.turn_off_sendind(1)
# Sqlighter.add_tag_to_id(123123, "#HashTag")