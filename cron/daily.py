import pymysql
import telebot
import os
import random
import time
token = ''
bot = telebot.TeleBot(token, skip_pending = True, threaded= False ,num_threads= 1)       
def on_db():
    db = pymysql.connect(host='localhost',
                         user='',
                         password='',                             
                         db='cards',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    return db


def a():
    db = on_db()
    with db.cursor() as cursor:
        sql = "UPDATE users SET balance = balance + 3 WHERE killA > 9"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET balance = balance + 3 WHERE killD > 9"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET balance = balance + 3 WHERE killM > 9"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET balance = balance + 3 WHERE dmgA > 99"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET balance = balance + 3 WHERE dmgD > 99"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET balance = balance + 3 WHERE dmgM > 99"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET balance = balance + 3 WHERE dmgO > 99"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET balance = balance + 3 WHERE winsD > 4"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET balance = balance + 4 WHERE playD > 14"
        cursor.execute(sql)
        db.commit()
        

        sql = "UPDATE users SET killA = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET killD = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET killM = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET dmgA = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET dmgD = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET dmgM = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET dmgO = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET winsD = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET playD = 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET premium = premium - 1 WHERE premium > 0"
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE users SET premGets = 0 WHERE premGets = 1"
        cursor.execute(sql)
        db.commit()


a()