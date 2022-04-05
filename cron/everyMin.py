import pymysql
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

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
        sql = "SELECT * FROM matches WHERE status IN (1, 2)"
        cursor.execute(sql)
        matches = cursor.fetchall()
        for _match in matches:
            sql = "SELECT * FROM matches WHERE id = %s"
            cursor.execute(sql, _match['id'])
            match = cursor.fetchone()
            if _match['status'] == match['status']:
                if _match['timeStat'] == match['timeStat']:
                    if int(time.time()) > match['timeStat']:
                        if match['status'] == 1:
                            sql = "UPDATE matches SET status = 2 WHERE id = %s"
                            cursor.execute(sql, (match['id']))
                            db.commit()
                            timeStat = int(time.time()) + 180
                            sql = "UPDATE matches SET timeStat = %s WHERE id = %s"
                            cursor.execute(sql, (timeStat, match['id']))
                            db.commit()
                            sql = "UPDATE matches SET p2Mana = p2Mana + 1 WHERE id = %s"
                            cursor.execute(sql, (match['id']))
                            db.commit()
                            sql = "SELECT * FROM users WHERE id = %s"
                            cursor.execute(sql, (match['player1']))
                            p1 = cursor.fetchone()
                            try:
                                bot.send_message(p1['user_id'], "Вам был засчитан пропуск хода из-за AFK.")
                            except:
                                pass
                            sql = "SELECT * FROM users WHERE id = %s"
                            cursor.execute(sql, (match['player2']))
                            p2 = cursor.fetchone()
                            try:
                                markup = InlineKeyboardMarkup()
                                markup.row_width = 2
                                markup.add(InlineKeyboardButton('Начать ход.', callback_data="match_view"))
                                bot.send_message(p2['user_id'], "Ваш оппонент пропускает ход. Настал ваш черёд.", reply_markup=markup)
                            except:
                                pass

                        elif match['status'] == 2:
                            sql = "UPDATE matches SET status = 1 WHERE id = %s"
                            cursor.execute(sql, (match['id']))
                            db.commit()
                            timeStat = int(time.time()) + 180
                            sql = "UPDATE matches SET timeStat = %s WHERE id = %s"
                            cursor.execute(sql, (timeStat, match['id']))
                            db.commit()
                            sql = "UPDATE matches SET p1Mana = p1Mana + 1 WHERE id = %s"
                            cursor.execute(sql, (match['id']))
                            db.commit()
                            sql = "SELECT * FROM users WHERE id = %s"
                            cursor.execute(sql, (match['player2']))
                            p2 = cursor.fetchone()
                            try:
                                bot.send_message(p2['user_id'], "Вам был засчитан пропуск хода из-за AFK.")
                            except:
                                pass
                            sql = "SELECT * FROM users WHERE id = %s"
                            cursor.execute(sql, (match['player1']))
                            p1 = cursor.fetchone()
                            try:
                                markup = InlineKeyboardMarkup()
                                markup.row_width = 2
                                markup.add(InlineKeyboardButton('Начать ход.', callback_data="match_view"))
                                bot.send_message(p1['user_id'], "Ваш оппонент пропускает ход. Настал ваш черёд.", reply_markup=markup)
                            except:
                                pass
        







def calculate_win(player1, player2, winner, match):
    db = on_db()
    with db.cursor() as cursor:

        if winner['id'] == player1['id']:
            if player1['elo'] - player2['elo'] < -800:
                winPts = 40
            elif player1['elo'] - player2['elo'] < -750:
                winPts = 39
            elif player1['elo'] - player2['elo'] < -700:
                winPts = 38
            elif player1['elo'] - player2['elo'] < -650:
                winPts = 37
            elif player1['elo'] - player2['elo'] < -600:
                winPts = 36
            elif player1['elo'] - player2['elo'] < -550:
                winPts = 35
            elif player1['elo'] - player2['elo'] < -500:
                winPts = 34
            elif player1['elo'] - player2['elo'] < -450:
                winPts = 33
            elif player1['elo'] - player2['elo'] < -400:
                winPts = 32
            elif player1['elo'] - player2['elo'] < -350:
                winPts = 31
            elif player1['elo'] - player2['elo'] < -300:
                winPts = 30
            elif player1['elo'] - player2['elo'] < -250:
                winPts = 29
            elif player1['elo'] - player2['elo'] < -200:
                winPts = 28
            elif player1['elo'] - player2['elo'] < -150:
                winPts = 27
            elif player1['elo'] - player2['elo'] < -100:
                winPts = 26
            elif player1['elo'] - player2['elo'] < 100:
                winPts = 25
            elif player1['elo'] - player2['elo'] < 150:
                winPts = 24
            elif player1['elo'] - player2['elo'] < 200:
                winPts = 23
            elif player1['elo'] - player2['elo'] < 250:
                winPts = 22
            elif player1['elo'] - player2['elo'] < 300:
                winPts = 21
            elif player1['elo'] - player2['elo'] < 350:
                winPts = 20
            elif player1['elo'] - player2['elo'] < 400:
                winPts = 19
            elif player1['elo'] - player2['elo'] < 450:
                winPts = 18
            elif player1['elo'] - player2['elo'] < 500:
                winPts = 17
            elif player1['elo'] - player2['elo'] < 550:
                winPts = 16
            elif player1['elo'] - player2['elo'] < 600:
                winPts = 15
            elif player1['elo'] - player2['elo'] < 650:
                winPts = 14
            elif player1['elo'] - player2['elo'] < 700:
                winPts = 13
            elif player1['elo'] - player2['elo'] < 750:
                winPts = 12
            elif player1['elo'] - player2['elo'] < 800:
                winPts = 11
            elif player1['elo'] - player2['elo'] > 850:
                winPts = 10
            else:
                winPts = 5


        elif winner['id'] == player2['id']:
            if player2['elo'] - player1['elo'] < -800:
                winPts = 40
            elif player2['elo'] - player1['elo'] < -750:
                winPts = 39
            elif player2['elo'] - player1['elo'] < -700:
                winPts = 38
            elif player2['elo'] - player1['elo'] < -650:
                winPts = 37
            elif player2['elo'] - player1['elo'] < -600:
                winPts = 36
            elif player2['elo'] - player1['elo'] < -550:
                winPts = 35
            elif player2['elo'] - player1['elo'] < -500:
                winPts = 34
            elif player2['elo'] - player1['elo'] < -450:
                winPts = 33
            elif player2['elo'] - player1['elo'] < -400:
                winPts = 32
            elif player2['elo'] - player1['elo'] < -350:
                winPts = 31
            elif player2['elo'] - player1['elo'] < -300:
                winPts = 30
            elif player2['elo'] - player1['elo'] < -250:
                winPts = 29
            elif player2['elo'] - player1['elo'] < -200:
                winPts = 28
            elif player2['elo'] - player1['elo'] < -150:
                winPts = 27
            elif player2['elo'] - player1['elo'] < -100:
                winPts = 26
            elif player2['elo'] - player1['elo'] < 100:
                winPts = 25
            elif player2['elo'] - player1['elo'] < 150:
                winPts = 24
            elif player2['elo'] - player1['elo'] < 200:
                winPts = 23
            elif player2['elo'] - player1['elo'] < 250:
                winPts = 22
            elif player2['elo'] - player1['elo'] < 300:
                winPts = 21
            elif player2['elo'] - player1['elo'] < 350:
                winPts = 20
            elif player2['elo'] - player1['elo'] < 400:
                winPts = 19
            elif player2['elo'] - player1['elo'] < 450:
                winPts = 18
            elif player2['elo'] - player1['elo'] < 500:
                winPts = 17
            elif player2['elo'] - player1['elo'] < 550:
                winPts = 16
            elif player2['elo'] - player1['elo'] < 600:
                winPts = 15
            elif player2['elo'] - player1['elo'] < 650:
                winPts = 14
            elif player2['elo'] - player1['elo'] < 700:
                winPts = 13
            elif player2['elo'] - player1['elo'] < 750:
                winPts = 12
            elif player2['elo'] - player1['elo'] < 800:
                winPts = 11
            elif player2['elo'] - player1['elo'] > 850:
                winPts = 10
            else:
                winPts = 5
        if winner['id'] == player1['id']:

            sql = "UPDATE users SET elo = elo + %s WHERE id = %s"
            cursor.execute(sql, (winPts, winner['id']))
            db.commit()
            sql = "UPDATE users SET hp = hp WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()
            sql = "UPDATE users SET pvpPlayed = pvpPlayed + 1 WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()
            sql = "UPDATE users SET pvpWins = pvpWins + 1 WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()
            sql = "UPDATE users SET winsD = winsD + 1 WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()
            sql = "UPDATE users SET playD = playD + 1 WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()

            sql = "UPDATE users SET elo = elo - %s WHERE id = %s"
            cursor.execute(sql, (winPts, player2['id']))
            db.commit()
            sql = "UPDATE users SET hp = hp WHERE id = %s"
            cursor.execute(sql, (player2['id']))
            db.commit()
            sql = "UPDATE users SET pvpPlayed = pvpPlayed + 1 WHERE id = %s"
            cursor.execute(sql, (player2['id']))
            db.commit()
            sql = "UPDATE users SET pvpLose = pvpLose + 1 WHERE id = %s"
            cursor.execute(sql, (player2['id']))
            db.commit()
            sql = "UPDATE users SET playD = playD + 1 WHERE id = %s"
            cursor.execute(sql, (player2['id']))
            db.commit()
        elif winner['id'] == player2['id']:
    
            sql = "UPDATE users SET elo = elo + %s WHERE id = %s"
            cursor.execute(sql, (winPts, winner['id']))
            db.commit()
            sql = "UPDATE users SET hp = hp WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()
            sql = "UPDATE users SET pvpPlayed = pvpPlayed + 1 WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()
            sql = "UPDATE users SET pvpWins = pvpWins + 1 WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()
            sql = "UPDATE users SET winsD = winsD + 1 WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()
            sql = "UPDATE users SET playD = playD + 1 WHERE id = %s"
            cursor.execute(sql, (winner['id']))
            db.commit()

            sql = "UPDATE users SET elo = elo - %s WHERE id = %s"
            cursor.execute(sql, (winPts, player1['id']))
            db.commit()
            sql = "UPDATE users SET hp = hp WHERE id = %s"
            cursor.execute(sql, (player1['id']))
            db.commit()
            sql = "UPDATE users SET pvpPlayed = pvpPlayed + 1 WHERE id = %s"
            cursor.execute(sql, (player1['id']))
            db.commit()
            sql = "UPDATE users SET pvpLose = pvpLose + 1 WHERE id = %s"
            cursor.execute(sql, (player1['id']))
            db.commit()
            sql = "UPDATE users SET playD = playD + 1 WHERE id = %s"
            cursor.execute(sql, (player1['id']))
            db.commit()




        sql = "UPDATE inventory SET nowhp = hp WHERE idplayer = %s"
        cursor.execute(sql, (player1['id']))
        db.commit()
        sql = "UPDATE inventory SET nowhp = hp WHERE idplayer = %s"
        cursor.execute(sql, (player2['id']))
        db.commit()


        sql = "UPDATE matches SET status = 5 WHERE id = %s"
        cursor.execute(sql, (match['id']))
        db.commit()
        sql = "UPDATE matches SET winner = %s WHERE id = %s"
        cursor.execute(sql, (winner['id'], match['id']))
        db.commit()

        sql = "UPDATE users SET hp = 50 WHERE id = %s"
        cursor.execute(sql, (match['player1']))
        db.commit()
        sql = "UPDATE users SET hp = 50 WHERE id = %s"
        cursor.execute(sql, (match['player2']))
        db.commit()

a()

def ladders():
    db = on_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM ladders WHERE active = 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for ladder in result:
                if int(time.time()) >= ladder['startDate']:
                    sql = "UPDATE ladders SET active = 2 WHERE id = %s"
                    cursor.execute(sql, (ladder['id']))
                    db.commit()
                    sql = "SELECT user_id FROM users WHERE ladder = %s"
                    cursor.execute(sql, (ladder['id']))
                    users = cursor.fetchall()
                    if users:
                        for user in users:
                            try:
                                bot.send_message(user['user_id'], f"Ладдер {ladder['name']} был запущен.")
                            except:
                                pass
        sql = "SELECT * FROM ladders WHERE active = 2"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for ladder in result:
                if int(time.time()) >= ladder['stopDate']:
                    sql = "UPDATE ladders SET active = 3 WHERE id = %s"
                    cursor.execute(sql, (ladder['id']))
                    db.commit()
                    sql = "SELECT * FROM users WHERE ladder = %s ORDER BY ladderPts DESC Limit 1"
                    cursor.execute(sql, (ladder['id']))
                    winner = cursor.fetchone()
                    try:
                        bot.send_message(winner['user_id'], f"Поздравляем с победой в ладдере {ladder['name']}! Награда уже зачислена!\nПриятной игры!")
                    except:
                        pass
                    sql = "UPDATE users SET balance = balance + %s WHERE id = %s"
                    cursor.execute(sql, (ladder['reward'], winner['id']))
                    db.commit()
                    sql = "UPDATE ladders SET winner = %s WHERE id = %s"
                    cursor.execute(sql, (winner['id'], ladder['id']))
                    db.commit()
        db.close()


ladders()