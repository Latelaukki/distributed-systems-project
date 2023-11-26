import os 
import sqlite3


def get_messages(db_path):
    db_con = make_db_con(db_path)
    cur = db_con.cursor()
    res = cur.execute("SELECT msg FROM message")
    messages = res.fetchall()
    cur.close()
    db_con.close()

    
    return messages


def store_message(params):
    db_path = params["db_path"]
    msg = params["msg"]

    db_con = make_db_con(db_path)
    cur = db_con.cursor()
    cur.execute("INSERT INTO message VALUES (?)", (msg,))
    db_con.commit()
    cur.close()
    db_con.close()


def make_db_con(db_path):
    return sqlite3.connect(db_path)

    
def init_db(db_path):

    con = make_db_con(db_path)
    cur = con.cursor()

    cur.execute("""
            CREATE TABLE IF NOT EXISTS message(
                msg TEXT NOT NULL
            );
    """)

    con.commit()
    cur.close()
    con.close()
