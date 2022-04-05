

async def profile(m, user):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('Профиль')
    item2 = types.KeyboardButton('Поиск')
    item3 = types.KeyboardButton('Инвентарь')
    item4 = types.KeyboardButton('Колода')
    item5 = types.KeyboardButton('Таверна')
    markup.row(item1, item5)
    markup.row(item3, item4)
    markup.row(item2)
    pvpWins = await db.Matches.filter(winner=user.id).count()
    pvpPlayed = await db.Matches.filter(Q(player1=user.id) | Q(player2=user.id)).count()
    pvpLose = await db.Matches.filter(Q(player1=user.id) | Q(player2=user.id), ~Q(winner=user.id), status=5).count()
    if m.chat.id != m.from_user.id: return
    if user.league == 1: league = "Бронза"
    elif user.league == 2: league = "Железо"
    elif user.league == 3: league = "Серебро"
    elif user.league == 4: league = "Золото"
    elif user.league == 5: league = "Алмаз"
    elif user.league == 6: league = "Платина"
    if user:
        text = """👤Профиль игрока {}
{}💰
{}✴️

Лига: {}

Дуэлей: {}
Побед: {}
Поражений: {}

🆔 - {}
        

Последние 5 Ranked-игр:

""".format(user.username, user.balance, user.elo, league, pvpPlayed, pvpWins, pvpLose, user.id)
        games = await db.Matches.filter(Q(player1=user.id) | Q(player2=user.id), status=5, tournament='matchmaking').order_by('-id').limit(5)
        for game in games:
            if game.winner == user.id: result = "✅"
            else: result = "❌"
            if game.player1 == user.id: versus = await db.Users.get_or_none(id=game.player2).only('username')
            if game.player2 == user.id: versus = await db.Users.get_or_none(id=game.player1).only('username')
            if versus:
                text += "\n{} vs {} ({})".format(user.username, versus.username, result)
        await bot.send_message(m.chat.id, text, reply_markup=markup)
    else:
        await start(m)
async def inventory(m, user):
    if m.chat.id != m.from_user.id: return
    if user:
        text = "Используемые карты:\n\n"
        items = await db.Inventory.exists(idplayer=user.id, status=2)
        if items:
            allItems = await db.Inventory.filter(idplayer=user.id, status=2).order_by('-rare')
            for z in allItems:
                if z.type == 'Охотник': Type = "🗡"
                elif z.type == 'Защитник': Type = "🛡"
                elif z.type == 'Маг': Type = '🔮'
                elif z.type == 'Особый': Type = "🌟"
                text += "{}{} ({}⭐️) - /view_{}\n".format(Type, z.name, z.rare, z.id)
        else:
            text += "Карты в колоде отсутствуют"

        text += "\n\nДоступные карты:\n\n"
        items = await db.Inventory.exists(idplayer=user.id, status=1)
        if items:
            allItems = await db.Inventory.filter(idplayer=user.id, status=1).order_by('-rare')
            for z in allItems:
                if z.type == 'Охотник': Type = "🗡"
                elif z.type == 'Защитник': Type = "🛡"
                elif z.type == 'Маг': Type = '🔮'
                elif z.type == 'Особый': Type = "🌟"
                text += "{}{} ({}⭐️) - /view_{}\n".format(Type, z.name, z.rare, z.id)
        else:
            text += "К сожалению, у тебя нет доступных карт."
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Множественное распыление', callback_data="selectDestroy"))

    if len(text) > 4096:
        l = len(text) + 1
        part_1 = text[0:l//2]
        part_2 = text[l//2:]

        await bot.send_message(user.user_id, f'{part_1}')
        await asyncio.sleep(1)
        await bot.send_message(user.user_id, f'{part_2}', reply_markup=markup)
    else:
        await bot.send_message(user.user_id, text, reply_markup=markup)
#Callback
@dp.callback_query_handler(lambda call: call.data.startswith('inventory'))
async def inventoryCall(call):
    if call.message.chat.id != call.from_user.id: return
    user = await db.Users.get_or_none(user_id=call.from_user.id).first()
    if user:
        text = "Используемые карты:\n\n"
        items = await db.Inventory.exists(idplayer=user.id, status=2)
        if items:
            allItems = await db.Inventory.filter(idplayer=user.id, status=2).order_by('-rare')
            for z in allItems:
                if z.type == 'Охотник': Type = "🗡"
                elif z.type == 'Защитник': Type = "🛡"
                elif z.type == 'Маг': Type = '🔮'
                elif z.type == 'Особый': Type = "🌟"
                text += "{}{} ({}⭐️) - /view_{}\n".format(Type, z.name, z.rare, z.id)
        else:
            text += "Карты в колоде отсутствуют"

        text += "\n\nДоступные карты:\n\n"
        items = await db.Inventory.exists(idplayer=user.id, status=1)
        if items:
            allItems = await db.Inventory.filter(idplayer=user.id, status=1).order_by('-rare')
            for z in allItems:
                if z.type == 'Охотник': Type = "🗡"
                elif z.type == 'Защитник': Type = "🛡"
                elif z.type == 'Маг': Type = '🔮'
                elif z.type == 'Особый': Type = "🌟"
                text += "{}{} ({}⭐️) - /view_{}\n".format(Type, z.name, z.rare, z.id)
        else:
            text += "К сожалению, у тебя нет доступных карт."
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Множественное распыление', callback_data="selectDestroy"))

    if len(text) > 4096:
        l = len(text) + 1
        part_1 = text[0:l//2]
        part_2 = text[l//2:]

        await bot.send_message(user.user_id, f'{part_1}')
        await asyncio.sleep(1)
        await bot.send_message(user.user_id, f'{part_2}', reply_markup=markup)
    else:
        await bot.send_message(user.user_id, text, reply_markup=markup)

async def view_(m, user):
    if m.chat.id != m.from_user.id: return
    if user:
        result = m.text.replace('/view_', '', 1).replace('@TowerOfHeaven_bot', '', 1)
        card = await db.Inventory.get_or_none(id=result).first()
        if card and card.idplayer == user.id:
            getHero = await db.Heroes.get(id=card.idHero).first()
            await db.send_pic(user, getHero)
            if card.idplayer == user.id:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                if card.status == 1:
                    markup.add(InlineKeyboardButton('Добавить в колоду', callback_data="poolEdit_{}".format(card.id)))
                elif card.status == 2:
                    markup.add(InlineKeyboardButton('Убрать из колоды', callback_data="poolEdit_{}".format(card.id)))
                markup.add(InlineKeyboardButton('Распылить (+{}💰)'.format(getHero.priceDestroy), callback_data="destroy_{}".format(card.id)))
                markup.add(InlineKeyboardButton('Вернуться в инвентарь', callback_data="inventory"))
                await bot.send_message(m.chat.id, "Выбери, что сделать с этой картой", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith('destroy_'))
async def destroy_(call):
    idCard = call.data.split("_")[1]
    user = await db.Users.get(user_id=call.from_user.id)
    if user:
        checkBattles = await db.Matches.exists(Q(player1=user.id) | Q(player2=user.id), ~Q(status=5))
        if checkBattles: return await bot.edit_message_text("У вас активна партия, необходимо сначала закончить её!", call.message.chat.id, call.message.message_id)
        card = await db.Inventory.get_or_none(id=idCard)
        if card and card.idplayer == user.id and card.status != 0:
            getHero = await db.Heroes.get(id=card.idHero).first()
            await db.Users.filter(id=user.id).update(balance=F('balance') + getHero.priceDestroy)
            await db.Inventory.filter(id=card.id).update(status=0)
            await bot.edit_message_text("Карта {} была распылена.\n+{}💰".format(card.name, getHero.priceDestroy), call.message.chat.id, call.message.message_id)
        else:
            await bot.edit_message_text("Такой карты не существует!", call.message.chat.id, call.message.message_id)

@dp.callback_query_handler(lambda call: call.data.startswith('selectDestroy'))
async def selectDestroy(call):
    user = await db.Users.get(user_id=call.from_user.id)
    if user:
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Распылить все 1⭐️', callback_data="allDestroy_1"))
        markup.add(InlineKeyboardButton('Распылить все 2⭐️', callback_data="allDestroy_2"))
        markup.add(InlineKeyboardButton('Распылить все 3⭐️', callback_data="allDestroy_3"))
        await bot.edit_message_text("Множественное распыление распыляет все карты выбранной редкости кроме находящихся в колоде", call.message.chat.id, call.message.message_id, reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data.startswith('allDestroy_'))
async def allDestroy_(call):
    user = await db.Users.get(user_id=call.from_user.id)
    if user:
        rare = call.data.split("_")[1]
        allCards = await db.Inventory.filter(idplayer=user.id, status=1, rare=int(rare))
        await bot.edit_message_text("Начался процесс распыления...", call.message.chat.id, call.message.message_id)
        profit = 0
        for card in allCards:
            checkCard = await db.Inventory.get_or_none(id=card.id)
            if checkCard.status == 1:
                hero = await db.Heroes.get(id=checkCard.idHero)
                await db.Inventory.filter(id=checkCard.id).update(status=0)
                await db.Users.filter(id=user.id).update(balance=F('balance') + hero.priceDestroy)
                profit += hero.priceDestroy
        await bot.send_message(user.user_id, "Распыление всех {}⭐️ завершено. Получено {}💰".format(rare, profit))


async def pool(m, user):
    if m.chat.id != m.from_user.id: return
    if user:
        cardsCount = await db.Inventory.filter(idplayer=user.id, status=2).count()
        text = "Используемые карты ({}/15):\n\n".format(cardsCount)
        if cardsCount > 0:
            allItems = await db.Inventory.filter(idplayer=user.id, status=2).order_by('rare')
            nowRare = 2
            for z in allItems:
                if nowRare != z.rare:
                    nowRare = z.rare
                    text += "\n"
                    for i in range(0, nowRare):
                        text += "⭐️"
                    text += "\n"
                if z.type == 'Охотник': Type = "🗡"
                elif z.type == 'Защитник': Type = "🛡"
                elif z.type == 'Маг': Type = '🔮'
                elif z.type == 'Особый': Type = "🌟"
                text += "{} {} (❤️{}/⚔️{}/⚡️{}) - /view_{}\n".format(Type, z.name, z.hp, z.atk, z.rare, z.id)
        else:
            text += "К сожалению, у тебя нет доступных карт."
        await bot.send_message(user.user_id, text)

@dp.callback_query_handler(lambda call: call.data.startswith('poolEdit_'))
async def poolEdit_(call):
    user = await db.Users.get(user_id=call.from_user.id)
    checkBattles = await db.Matches.exists(Q(player1=user.id) | Q(player2=user.id), ~Q(status=5))
    if checkBattles: return await bot.edit_message_text("У вас активна партия, необходимо сначала закончить её!", call.message.chat.id, call.message.message_id)
    idCard = call.data.split("_")[1]
    if user:
        card = await db.Inventory.get_or_none(id=idCard)
        if card and card.idplayer == user.id and card.status != 0:
            if card.status == 1: 
                countInPool = await db.Inventory.filter(idplayer=user.id, status=2).count()
                if countInPool < 15:
                    card.status = 2
                    text = "Карта {} добавлена в колоду.".format(card.name)
                else:
                    text = "Колода забита, максимум 15 карт!"
            else:
                card.status = 1
                text = "Карта {} убрана из колоды.".format(card.name)
            await card.save()
        else:
            text = "Карта принадлежит не вам"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        await inventoryCall(call)



async def dailyStats(call, user):
    text = "Ежедневные задания - выполняйте задания и получайте 💰 за выполнение! Награды за выполненые задания выдаются каждые сутки в 03:00 МСК\nСписок заданий:"
    if user.killA >= 10: result = "✅"
    else: result = f"{user.killA}/10 (3💰)"
    text += "\n\nПобеждено охотников: {}".format(result)
    
    if user.killD >= 10: result = "✅"
    else: result = f"{user.killD}/10 (3💰)"
    text += "\nПобеждено защитников: {}".format(result)
    
    if user.killM >= 10: result = "✅"
    else: result = f"{user.killM}/10 (3💰)"
    text += "\nПобеждено магов: {}".format(result)
    
    if user.dmgA >= 100: result = "✅"
    else: result = f"{user.dmgA}/100 (3💰)"
    text += "\nНанесено урона охотниками: {}".format(result)
    
    if user.dmgD >= 100: result = "✅"
    else: result = f"{user.dmgD}/100 (3💰)"
    text += "\nНанесено урона защитниками: {}".format(result)
    
    if user.dmgM >= 100: result = "✅"
    else: result = f"{user.dmgM}/100 (3💰)"
    text += "\nНанесено урона магами: {}".format(result)

    if user.dmgO >= 100: result = "✅"
    else: result = f"{user.dmgO}/100 (3💰)"
    text += "\nНанесено урона особыми: {}".format(result)

    if user.winsD >= 5: result = "✅"
    else: result = f"{user.winsD}/5 (3💰)"
    text += "\nВыиграно партий: {}".format(result)

    if user.dmgA >= 15: result = "✅"
    else: result = f"{user.playD}/15 (4💰)"
    text += "\nСыграно партий: {}".format(result)
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)








async def donate(m):
    if m.chat.id != m.from_user.id: return
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if user:
        text = """Вы можете поддержать дальнейшую разработку и развитие проекта материально (https://toh.su/donate_anikado) . За поддержку проекта можно получить 💰, сумма которых будет равна вашему пожертвованию в рублях. 

Ваша поддержка помогает разработчику не останавливаться и продолжать разработку, ну и, знаете... жить.

Ваш внутриигровой ID - {}
Зачисление 💰 происходит в автоматическом режиме.""".format(user.id)
        await m.reply(text)
    else:
        await start(m)


