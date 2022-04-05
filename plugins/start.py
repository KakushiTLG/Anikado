
async def register_cards(user):
    for i in range(3, 18):
        hero = await db.Heroes.get_or_none(id=i)
        countInPool = await db.Inventory.filter(idplayer=user.id, status=2).count()
        if countInPool <= 14:
            newCard = await db.Inventory.create(idHero=hero.id, idplayer=user.id, name=hero.name, type=hero.type, rare=hero.rare, hp=hero.hp, nowhp=hero.hp, atk=hero.atk, status=2)
        else:
            newCard = await db.Inventory.create(idHero=hero.id, idplayer=user.id, name=hero.name, type=hero.type, rare=hero.rare, hp=hero.hp, nowhp=hero.hp, atk=hero.atk, status=1)
    print('done')
    await asyncio.sleep(30)
    try: await bot.send_message(user.user_id, "Ваша стартовая колода уже готова! Вы можете управлять ею через меню.")
    except: pass

async def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None

async def start(m):
    if m.chat.id != m.from_user.id: return
    checkUser = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if checkUser:
        await profile(m, checkUser)
    else:
        if m.from_user.id in backup.users:
            _id = backup.users[m.from_user.id]['id']
            elo = backup.users[m.from_user.id]['elo']
            balance = backup.users[m.from_user.id]['balance']
            donateSum = backup.users[m.from_user.id]['donateSum']
            ref = backup.users[m.from_user.id]['ref']
            username = backup.users[m.from_user.id]['username']
            newUser = await db.Users.create(id=_id,
                user_id=m.from_user.id,
                elo=elo,
                balance=balance,
                donateSum=donateSum,
                ref=ref,
                username=username
            )
            await m.answer("Прогресс восстановлен. Приятной игры!")
            await asyncio.sleep(1)
            checkref = False
        else:
            unique_code = await extract_unique_code(m.text)
            checkref = await db.Users.get_or_none(user_id=unique_code)
            if checkref:
                ref = unique_code
            else:
                ref = 702528084
            newUser = await db.Users(user_id=m.from_user.id, username=m.from_user.first_name, ref=ref)
            await newUser.save()
            await bot.send_message(m.chat.id, "Добро пожаловать в Anikado - рейтинговая карточная игра где собраны персонажи из многих известных аниме! На данный момент игра находится в стадии открытого бета-тестирования, а значит могут наблюдаться небольшие ошибки, проблемы, очепятки и тд и тп, но это всё достаточно быстро исправляется!")
            await asyncio.sleep(5)
        text = "Желаете пройти обучение?"
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        item1 = types.KeyboardButton('Пройти обучение')
        item2 = types.KeyboardButton('Отказаться от обучения')
        markup.row(item1, item2)
        await bot.send_message(m.chat.id, text, reply_markup=markup)
        await bot.send_message(kakushigoto, "New user: @{} \n{}\nRef {}".format(m.from_user.username, m.from_user.id, ref))
        if checkref:
            await bot.send_message(checkref.user_id, "По твоей ссылке зарегистрировался {}".format(m.from_user.first_name))
        await register_cards(newUser)



async def start_start(m, user):
    if m.chat.id != m.from_user.id: return
    checkUser = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if checkUser:
        await m.answer("Приятной игры!")
        await asyncio.sleep(1)
        await profile(m, checkUser)


async def start_1(m, user):
    text = """👤Профиль игрока {}
200💰
1000✴️

Лига: Серебро

Дуэлей: 0
Побед: 0
Поражений: 0

🆔 - {}""".format(user.username, user.id)
    await bot.send_message(m.chat.id, text)
    await asyncio.sleep(3)
    text = """Это твой профиль. 💰 - ресурс, который можно тратить, открывая новые карты в разделе "Таверна".
✴️ - твои очки рейтинга. В игре присутствует система лиг, при наличии достижений в текущей лиге, игрок переходит в следующую.
Всего в игре шесть лиг, для перехода в следующую необходимо набрать 2000✴️ в рейтинговых боях.
Если количество очков в конце сезона(месяца) будет ниже 750✴️, игрок падает в лигу ниже уровня.
Если у игрока не хватает очков для перехода в следующую лигу, но так же и хватает очков дабы не упасть в лигу ниже, он остаётся в старой лиге в новом сезоне.

Теперь перейдём к самим картам?"""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton('Перейти к картам')
    item2 = types.KeyboardButton('Отказаться от обучения')
    markup.row(item1, item2)
    await bot.send_message(m.chat.id, text, reply_markup=markup)


async def start_2(m, user):
    text = """Все доступные карты хранятся в разделе "Инвентарь". Карты можно использовать в колоду, можно их продать за какое-то количество 💰 (распыление), а так же - узнать информацию о карте и её характеристики.

Управлять колодой можно через раздел "Колода". 
Все карты делятся на четыре типа:
Охотник - карта с преобладающим количеством характеристик атаки
Защитник - карта с преобладающим количеством характеристик здоровья, а так же - живой щит игрока (Пока у вас на столе есть живой защитник, карты противника не нанесут урон основному персонажу (есть исключения))
Маг - тип карт, которые можно комбинировать между собой, получая различные бонусы в партии.
Особый - карта, не имеющая характеристик, однако обладающая определённым эффектом, который может перевернуть ход партии.

Примечание: Карты можно использовать сразу после призыва на поле боя"""
    await bot.send_message(m.chat.id, text)
    await asyncio.sleep(5)
    text = """Так же у карт есть система редкости. Чем выше степень редкости, тем лучше её характеристики.
Всего есть 5 степеней редкости, от 1⭐️ до 5⭐️. На поле боя карты призываются с помощью энергии⚡️, которая накапливается каждый ход.
Затраты энергии на призыв карты равны степени редкости.

На этом краткий экскурс окончен. Если у вас возникнут дополнительные вопросы, вам всегда помогут в чате обсуждения проекта. Приятной игры!"""
    await bot.send_message(m.chat.id, text)
    await asyncio.sleep(5)
    await profile(m, user)
    await asyncio.sleep(2)
    await bot.send_message(m.chat.id, "Вы можете получить 50💰 за вступление в группу обсуждения игры! (@anikado_chat)")
