# -*- coding: utf-8 -*-
# coding: utf-8
import re
import json
import time
from os.path import exists
import logging
import os
import math
import threading
from threading import Timer
import engine as db
import random
import pymysql
import datetime
import telebot
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram import exceptions
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.query_utils import Q
from tortoise.expressions import F
import logger
import backup
devChat = -1001364436303

kakushigoto = 702528084
bot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#Подхват файлов
game_plugins = [ f[:-3] for f in os.listdir('plugins') if f.endswith('.py') ]
for plugin in game_plugins:
    try:
        exec(open("./plugins/" + plugin + ".py", encoding="utf-8").read())
        print ("Подключен " + plugin)
    except Exception as e:
        print("Ошибка подключения " + plugin) 
        print(str(e))
try:
    exec(open("./hand.py", encoding="utf-8").read())
except Exception as e:
    print(e)
# !
async def databasetimer():
    if not db.database.is_closed():
        db.database.close()
        db.database.connect()
        print("DB conn restart")
    await asyncio.sleep(3600)
    await databasetimer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
#import traceback
#while True:
#    try:
#        bot.polling(none_stop=True)
#    except Exception as e:
#        bot.send_message(kakushigoto, str(traceback.format_exc()))
#        print('\n\nRestart\n\n')
#        time.sleep(1)
        
