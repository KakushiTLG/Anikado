import asyncio

from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.query_utils import Q
import random
import time
from aiogram import Bot, Dispatcher, executor, types


#database = peewee.MySQLDatabase('megu', user='kakushigoto', password='d87ospdn1j', host='localhost', port=3306)

def ABC(length):
    output = ""
    for x in range(length):
        output += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890')
    return output



"""class Base(Model):

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return super(Base, cls).get(*args, **kwargs)
        except Exception as e:
            return False

    class Meta:
        database = database"""

class Matches(Model):
    id = fields.IntField(pk=True)
    tournament = fields.CharField(max_length=256, default='matchmaking')
    player1 = fields.IntField(default=0)
    player2 = fields.IntField(default=0)
    p1Mana = fields.IntField(default=1)
    p2Mana = fields.IntField(default=1)
    timeStat = fields.IntField(default=time.time())
    p1hero1 = fields.IntField(null=True)
    p1hero2 = fields.IntField(null=True)
    p1hero3 = fields.IntField(null=True)
    p1hero4 = fields.IntField(null=True)
    p1hero5 = fields.IntField(null=True)
    p2hero1 = fields.IntField(null=True)
    p2hero2 = fields.IntField(null=True)
    p2hero3 = fields.IntField(null=True)
    p2hero4 = fields.IntField(null=True)
    p2hero5 = fields.IntField(null=True)
    status = fields.IntField(default=0)
    winner = fields.IntField(default=-1)
    class Meta:
        table = 'matches'

class Inventory(Model):
    id = fields.IntField(pk=True)
    idHero = fields.IntField(default=0)
    idplayer = fields.IntField(default=0)
    name = fields.CharField(max_length=128)
    type = fields.CharField(max_length=128)
    rare = fields.IntField(default=1)
    status = fields.IntField(default=1)
    hp = fields.IntField(default=0)
    nowhp = fields.IntField(default=0)
    atk = fields.IntField(default=0)

    class Meta:
        table = 'inventory'

class Heroes(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    type = fields.CharField(max_length=128)
    rare = fields.IntField(default=0)
    hp = fields.IntField(default=0)
    atk = fields.IntField(default=0)
    priceDestroy = fields.IntField(default=0)
    descr = fields.CharField(max_length=4096)
    short_descr = fields.CharField(max_length=1024)
    class Meta:
        table = 'heroes'

class Users(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField(null=False)
    username = fields.CharField(max_length=128)
    balance = fields.IntField(default=200)
    almaz = fields.IntField(default=0)
    donateSum = fields.IntField(default=0)
    pvpPlayed = fields.IntField(default=0)
    pvpWins = fields.IntField(default=0)
    pvpLose = fields.IntField(default=0)
    hp = fields.IntField(default=50)
    elo = fields.IntField(default=1000)
    sleepPlayer = fields.IntField(default=time.time)
    ban = fields.IntField(default=0)
    akTV = fields.IntField(default=0)
    premium = fields.IntField(default=0)
    premGets = fields.IntField(default=0)
    league = fields.IntField(default=2)
    search = fields.IntField(default=0)
    killA = fields.IntField(default=0)
    killM = fields.IntField(default=0)
    killD = fields.IntField(default=0)
    killO = fields.IntField(default=0)
    dmgM = fields.IntField(default=0)
    dmgA = fields.IntField(default=0)
    dmgD = fields.IntField(default=0)
    dmgO = fields.IntField(default=0)
    winsD = fields.IntField(default=0)
    playD = fields.IntField(default=0)
    ladderPts = fields.IntField(default=0)
    ladder = fields.IntField(null=True)
    ref = fields.IntField(null=True)
    class Meta:
        table = 'users'


class Ladders(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    active = fields.IntField(default=1)
    startDate = fields.IntField(null=False)
    stopDate = fields.IntField(null=False)
    winner = fields.IntField(null=True)
    reward = fields.IntField(null=False)
    class Meta:
        table = 'ladders'


class System(Model):
    id = fields.IntField(pk=True)
    value = fields.IntField(null=False)
    name = fields.CharField(max_length=128)
    class Meta:
        table = 'system'



allCards = {1: [], 2: [], 3: [], 4: [], 5: []}
bot = Bot(token='2022915354:AAHwHvH50VNwkJo1oXe7N2-tcf2M-yA3Few')

async def get_db():
    print("Подключаемся к БД...")
    await Tortoise.init(db_url="mysql://user:psswd@localhost:3306/cards", modules={"models": ["engine"]})
    await Tortoise.generate_schemas()
    print("Составляем сборку карт...")
    _allCards = await Heroes.filter()
    for z in _allCards:
        allCards[z.rare].append(z.id)
    print("Сборка готова\n\n{}\n\n".format(allCards))

#loop = asyncio.get_event_loop()
#tort_db = loop.run_until_complete(get_db())




async def addCard(user, hero):
    card = await Heroes.get(id=hero)
    newCard = await Inventory(idplayer=user.id, idHero=hero, name=card.name, type=card.type, rare=card.rare, status=1, hp=card.hp, nowhp=card.hp, atk=card.atk)
    await newCard.save()
    return

async def send_pic(user, hero):
    try:
        photo = open('/home/kakushigoto/cards/media/characters/{}.jpg'.format(hero.id), 'rb')
        await bot.send_photo(user.user_id, photo, caption=hero.descr)
    except:
        await bot.send_message(user.user_id, "Героя не существует.")
    return