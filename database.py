import sqlite3
import datetime
import requests

from config import *


def get_db():
    db = sqlite3.connect("data.db")
    return db


def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS tokens(
                owner TEXT,
                token TEXT,
                get_date TEXT,
                out_date TEXT,
                canUse BOOL,
                email TEXT
            )
        """,
        """CREATE TABLE IF NOT EXISTS admins(
            id TEXT
        )"""
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
        db.commit()


def add_token(token: str, owner: str, out_date: str, email: str):
    db = get_db()
    cursor = db.cursor()

    if cursor.execute("SELECT * FROM tokens WHERE token = ? AND owner = ?", [token, owner]).fetchone() is None:
        statement = "INSERT INTO tokens VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(statement, [owner, token, datetime.datetime.now(), datetime.datetime.strptime(out_date, '%B %d, %Y, %H:%M:%S'), True, email])
        db.commit()
        return {'ok': True}
    else:
        return {'ok': False}


def delete_token(token: str):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM tokens WHERE token = ?"
    cursor.execute(statement, [token])
    db.commit()
    return True


def get_token_by_owner(owner: str):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT token FROM tokens WHERE owner = ?"
    cursor.execute(statement, [owner])
    return cursor.fetchone()


def get_owner_by_token(token: str):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT owner FROM tokens WHERE token = ?"
    cursor.execute(statement, [token])
    return cursor.fetchone()


def get_token_by_email(email: str):
    db = get_db()
    cursor = db.cursor()

    if cursor.execute("SELECT * FROM tokens WHERE email = ?", [email]).fetchone() is None:
        return "Not found!", None
    else:
        data = cursor.execute("SELECT * FROM tokens WHERE email = ?", [email]).fetchone()
        return {
            "owner": data[0],
            "createdData": data[2],
            "endDate": data[3],
            "canUse": data[4],
            "email": data[5]
        }


def get_token(token: str):
    db = get_db()
    cursor = db.cursor()

    if cursor.execute("SELECT * FROM tokens WHERE token = ?", [token]).fetchone() is None:
        return "Not found!"
    else:
        data = cursor.execute("SELECT * FROM tokens WHERE token = ?", [token]).fetchone()
        return {
            "owner": data[0],
            "createdData": data[2],
            "endDate": data[3],
            "canUse": data[4],
            "email": data[5]
        }
    
def get_token_small_info(token: str):
    db = get_db()
    cursor = db.cursor()

    if cursor.execute("SELECT * FROM tokens WHERE token = ?", [token]).fetchone() is None:
        return "NULL;false"
    else:
        data = cursor.execute("SELECT * FROM tokens WHERE token = ?", [token]).fetchone()
        if (data[4] == 0):
            return (f'{data[0]};false')
        else:
            return (f'{data[0]};true')


def register(email: str, url: str):
    db = get_db()
    cursor = db.cursor()

    if cursor.execute("SELECT * FROM tokens WHERE email = ?", [email]).fetchone() is None:
        text = f"EMail: {email}\nURL: {url}"
        for user in cursor.execute("SELECT id FROM admins"):
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user[0]}&text={text}")
        return {'ok': True}
    else:
        return False
