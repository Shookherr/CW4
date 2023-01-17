# Отдельная утилита создания БД пользователей (таблица user)
from dao.model.user import User, UserSchema
import sqlite3


u1 = User(email="vasya@mail.ru", password="my_little_pony", name="vasya", surname='qwe', favorite_genre=1)
u2 = User(email="oleg@mail.ru", password="qwerty",name="oleg", surname='qwe', favorite_genre=2)
u3 = User(email="oleg@gmail.com", password="P@ssw0rd", name="vasya", surname='qwe', favorite_genre=3)
u4 = User(email="monya@mail.ru", password="Biba", name="monya", surname='qwe', favorite_genre=4)

us = list()
us.append(u1)
us.append(u2)
us.append(u3)
us.append(u4)

uss = UserSchema(many=True).dump(us)

# Подключение к БД
with sqlite3.connect('..\movies.db') as connection:
    cursor = connection.cursor()
    query = """CREATE TABLE IF NOT EXISTS user 
    (id INTEGER PRIMARY KEY NOT NULL, 
    email VARCHAR(255), 
    password VARCHAR(255), 
    name VARCHAR(255),
    surname VARCHAR(255),
    favorite_genre INTEGER)"""
    cursor.execute(query)
    for i, u in enumerate(uss):
        query = f"""
        INSERT INTO user 
        VALUES ({i+1}, "{u['email']}", "{u['password']}", "{u['name']}", "{u['surname']}", "{u['favorite_genre']}")
        """
        cursor.execute(query)

    connection.commit()
