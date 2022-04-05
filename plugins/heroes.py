async def specialBox(m, user):
    if m.chat.id != m.from_user.id: return
    if user:
        allCards = await db.Heroes.filter().order_by('-id').limit(10)
        text = "Новые карточки, доступные в специальном боксе:\n\n\n"
        for z in allCards:
            text += "{} {} ({}⭐️) - {} (/globalView_{})\n\n".format(z.type, z.name, z.rare, z.short_descr, z.id)
        await bot.send_message(m.chat.id, text)

async def globalView_(m, user):
    if m.chat.id != m.from_user.id: return
    if user:
        try:
            result = m.text.replace('/globalView_', '', 1).replace('@Anikado_bot', '', 1)
            getHero = await db.Heroes.get_or_none(id=result).first()
        except:
            getHero = None
        if getHero:
            await db.send_pic(user, getHero)


async def boxes(m, user):
    if m.chat.id != m.from_user.id: return
    if user:
        text = "У тебя {}💰\nТекущие боксы:\n\nОбщий бокс (выпадают все доступные карточки) - 10💰".format(user.balance)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Открыть общий бокс (10💰)', callback_data="boxOpen_default"))
        markup.add(InlineKeyboardButton('Открыть общий бокс 10 раз (90💰)', callback_data="boxOpen_default_10"))
        #markup.add(InlineKeyboardButton('Открыть специальный бокс', callback_data="boxOpen_special"))
        await bot.send_message(m.chat.id, text, reply_markup=markup)

async def boxes(call, user):
    if user:
        text = "У тебя {}💰\nТекущие боксы:\n\nОбщий бокс (выпадают все доступные карточки) - 10💰".format(user.balance)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Открыть общий бокс (10💰)', callback_data="boxOpen_default"))
        markup.add(InlineKeyboardButton('Открыть общий бокс 10 раз (90💰)', callback_data="boxOpen_default_10"))
        #markup.add(InlineKeyboardButton('Открыть специальный бокс', callback_data="boxOpen_special"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith('boxOpen_'))
async def boxOpen_(call):
    selected = call.data.split("_")[1]
    user = await db.Users.get(user_id=call.from_user.id)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Открыть общий бокс (10💰)', callback_data="boxOpen_default"))
    markup.add(InlineKeyboardButton('Открыть общий бокс 10 раз (90💰)', callback_data="boxOpen_default_10"))
    #markup.add(InlineKeyboardButton('Открыть специальный бокс', callback_data="boxOpen_special"))
    if user:
        if selected == 'default':
            try:
                if call.data.split("_")[2]:
                    count = call.data.split("_")[2]
                    if count.isdigit():
                        if int(count) > 0:
                            await bot.edit_message_text("Начинаем открывать...", call.message.chat.id, call.message.message_id)
                            if int(count) == 10 and user.balance >= 90:
                                await db.Users.filter(id=user.id).update(balance=F('balance') + 10)
                                await user.refresh_from_db()
                    else:
                        count = 1
                else:
                    count = 1
            except:
                count = 1
            for i in range(0, int(count)):
                if user.balance >= 10:
                    rand = random.randint(1, 1000)
                    print(rand)
                    if rand <= 15: randomed = random.choice(db.allCards[5])
                    elif rand <= 100: randomed = random.choice(db.allCards[4])
                    elif rand <= 300: randomed = random.choice(db.allCards[3])
                    elif rand <= 600: randomed = random.choice(db.allCards[2])
                    elif rand <= 1000: randomed = random.choice(db.allCards[1])
                    winned = await db.Heroes.get(id=randomed).first()
                    await db.addCard(user, winned.id)
                    await db.Users.filter(id=user.id).update(balance=F('balance') - 10)
                    await user.refresh_from_db()
                    text = "Ты выигрываешь {} ({}⭐️)!".format(winned.name, winned.rare)
                    await asyncio.sleep(.5)
                else:
                    text = "У тебя не хватает 💰. Получить 💰 можно, выполняя ежедневные задания, побеждая в ладдерах или же с помощью /donate"
                    await bot.send_message(call.message.chat.id, text)
                    return
                await bot.send_message(call.message.chat.id, text)
            await bot.send_message(call.message.chat.id, "\n\nУ тебя {}💰\nТекущие боксы:\n\nОбщий бокс (выпадают все доступные карточки) - 10💰".format(user.balance), reply_markup=markup)
            return
        elif selected == 'special':
            if user.balance >= 20:
                lastCard = await db.Heroes.filter().order_by('-id').limit(1)
                lastId = lastCard[0].id
                firstId = lastId - 10
                rand = random.randint(firstId, lastId)
                winned = await db.Heroes.get(id=rand).first()
                await db.addCard(user, winned.id)
                await db.Users.filter(id=user.id).update(balance=F('balance') - 20)
                await user.refresh_from_db()
                text = "Ты выигрываешь {} ({}⭐️)!\n\nУ тебя {}💰\nТекущие боксы:\n\nОбщий бокс (выпадают все доступные карточки) - 10💰".format(winned.name, winned.rare, user.balance)
            else:
                text = "У тебя не хватает 💰. Получить 💰 можно, выполняя ежедневные задания, побеждая в ладдерах или же с помощью /donate"
        else:
            text = "Возникла ошибка. Такого бокса не существует."
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)






