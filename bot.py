import binascii
import datetime
import os
import sqlite3
import telebot

token = "6560702698:AAEnVRPy46l1frPvZXRry-TKl6PyGwH91Fk"
bot = telebot.TeleBot(token)

db = sqlite3.connect("data.db")

def get_db():
    db = sqlite3.connect("data.db")
    return db

def add_token(token: str, owner: str, email: str):
    db = get_db()
    cursor = db.cursor()

    if cursor.execute("SELECT * FROM tokens WHERE token = ? AND owner = ?", [token, owner]).fetchone() is None:
        statement = "INSERT INTO tokens VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(statement, [owner, token, datetime.datetime.now(), None, True, email])
        db.commit()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Для получения API доступа напишите @selezzz")

@bot.message_handler(content_types='text')
def text_message(message):
    if (message.text.startswith('create_token') and message.chat.id == 2115011712 or message.text.startswith('create_token') and message.chat.id == 992887429):
        words = message.text.split(' ')
        new_words = []
        for word in words:
            if "create_token" not in word:
                new_words.append(word)
        print(new_words)
        token = binascii.hexlify(os.urandom(25)).decode()
        owner = new_words[0]
        email = new_words[1]
        add_token(token=token, owner=owner, email=email)
        bot.send_message(message.chat.id, f'Ваш токен создан!\nНикому не говорите и не отправляйте его: <span class="tg-spoiler">{token}</span>\nВ случае "слива" токена его удалят и у вас не будет возможности его вернуть', parse_mode="HTML")
bot.infinity_polling()