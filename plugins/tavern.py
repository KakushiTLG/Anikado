async def tavern(m, user):
    text = "Добро пожаловать в таверну! Здесь ты можешь посмотреть топ лиги, сыграть в некоторые игры либо же поговорить по душам за кружкой хмельного!"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('ТОП лиги', callback_data="top_league"))
    markup.add(InlineKeyboardButton('Боксы', callback_data="boxes"))
    markup.add(InlineKeyboardButton('Задания', callback_data="daily"))
    markup.add(InlineKeyboardButton('Ладдеры', callback_data="ladders"))
    markup.add(InlineKeyboardButton('AnikadoTV', callback_data="akTv"))
    markup.add(InlineKeyboardButton('Premium-статус', callback_data="premium"))
    markup.add(InlineKeyboardButton('Пригласить друзей', callback_data="refs"))
    markup.add(InlineKeyboardButton('Общение', url="https://t.me/Anikado_chat"))
    await m.answer(text, reply_markup=markup)



async def top_league(call, user):
    top10 = await db.Users.filter(league=user.league).only('elo', 'username').order_by('-elo').limit(10)
    if user.league == 1: league = "Бронза"
    elif user.league == 2: league = "Железо"
    elif user.league == 3: league = "Серебро"
    elif user.league == 4: league = "Золото"
    elif user.league == 5: league = "Алмаз"
    elif user.league == 6: league = "Платина"

    text = "ТОП игроков лиги {}:\n".format(league)
    for usr in top10:
        text += "\n{} - {}✴️".format(usr.username, usr.elo)
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)



async def premium(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if user.premium == 0:
        text = "Premium-статус позволяет пользоваться просмотром игр в режиме реального времени, а так же получать 16💰 в день на протяжении месяца. Стоимость - 255руб."
        markup.add(InlineKeyboardButton('Приобрести Premium-статус', url="https://toh.su/anikado_premium"))
    else:
        text = "Ваш Premium активен еще {}дн".format(user.premium)
        if user.premGets == 0:
            markup.add(InlineKeyboardButton('Получить ежедневный бонус', callback_data="getBonusPrem"))
        markup.add(InlineKeyboardButton('Продлить Premium-статус', url="https://toh.su/anikado_premium"))
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


async def getBonusPrem(call, user):
    if user.premGets == 0 and user.premium > 0:
        await db.Users.filter(id=user.id).update(balance=F('balance') + 16, premGets=1)
        await bot.edit_message_text("Получено 16💰. Приходи завтра!", call.message.chat.id, call.message.message_id)
    elif user.premGets == 1 and user.premium > 0:
        await bot.edit_message_text("Ты уже получал бонус. Приходи завтра!", call.message.chat.id, call.message.message_id)
    else:
        await bot.edit_message_text("Бонус доступен только владельцам Premium-статуса. Подробнее в Таверне.", call.message.chat.id, call.message.message_id)



async def ladders(call, user):
    text = "Ладдеры - хороший способ подзаработать 💰. Вступайте в ладдеры, соревнуйтесь в ранговой игре, зарабатывая ладдер-очки и забирайте награду за победу в ладдере!"
    if user.ladder:
        checkLadder = await db.Ladders.get_or_none(id=user.ladder).first()
        if checkLadder and checkLadder.active in [1, 2]:
            text += f"\nВаш текущий ладдер: {checkLadder.name} (/ladder_{checkLadder.id})\n"
    _ladders = await db.Ladders.filter(~Q(active=3))
    text += "\nСписок запланированных/идущих ладдеров:\n\n(время указано в формате GMT. MSK = GMT+3)\n"
    if _ladders:
        for ladder in _ladders:
            if ladder.active==1: status = "⏳"
            elif ladder.active==2: status = "🏃‍♂️"
            text += f"\n{ladder.name} ({status}) - /ladder_{ladder.id}"
    else:
        text += "К сожалению, идущих ладдеров сейчас нет."
    _ladders = await db.Ladders.filter(active=3).order_by('-id').limit(5)
    if _ladders:
        text += "\n\nПрошедшие ладдеры:"
        for ladder in _ladders:
            winner = await db.Users.get_or_none(id=ladder.winner).first()
            if winner:
                text += f"\n{ladder.name} (☑️) - {winner.username}"
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    #markup.add(InlineKeyboardButton('Создать собственный ладдер', callback_data="createLadder")) создание своих ладдеров
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)


async def ladder_(m, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    ladder = await db.Ladders.get_or_none(id=m.text.split("_")[1]).first()
    if ladder:
        if ladder.active==1: status = "⏳"
        elif ladder.active==2: status = "🏃‍♂️"
        elif ladder.active==3: status = "☑️"
        text = f"Ладдер {ladder.name}\nСтатус: {status}"
        startTime = datetime.datetime.fromtimestamp(ladder.startDate)
        stopTime = datetime.datetime.fromtimestamp(ladder.stopDate)
        text += f"\nДата начала: {startTime}\nДата завершения: {stopTime}"
        text += f"\nНаграда: {ladder.reward}💰"
        if ladder.active==3:
            ladderWinner = await db.Users.get_or_none(id=ladder.winner)
            text += f"\nПобедитель: {ladderWinner.username}"
        if ladder.active in [1, 2]:
            if ladder.active==2:markup.add(InlineKeyboardButton('ТОП ладдера', callback_data="ladderTop_{}".format(ladder.id)))
            ladderCount = await db.Users.filter(ladder=ladder.id).only('id').count()
            text += f"\nКоличество участников: {ladderCount}"
            if user.ladder == ladder.id:
                text += f"\nВаши ладдер-очки: {user.ladderPts}"
                markup.add(InlineKeyboardButton('Покинуть ладдер', callback_data="ladderLeave_{}".format(ladder.id)))
            else:
                markup.add(InlineKeyboardButton('Вступить в ладдер', callback_data="ladderJoin_{}".format(ladder.id)))
        await bot.send_message(m.chat.id, text, reply_markup=markup)
    else:
        await bot.send_message(m.chat.id, "Такого ладдера не существует")

async def ladderLeave_(call, user):
    ladder = await db.Ladders.get_or_none(id=call.data.split("_")[1]).first()
    if ladder and user.ladder == ladder.id:
        await db.Users.filter(id=user.id).update(ladder=0, ladderPts=0)
        await bot.edit_message_text("Вы успешно покинули ладдер. Текущие очки обнулены", call.message.chat.id, call.message.message_id)
async def ladderJoin_(call, user):
    ladder = await db.Ladders.get_or_none(id=call.data.split("_")[1]).first()
    if ladder and user.ladder != ladder.id:
        await db.Users.filter(id=user.id).update(ladder=ladder.id, ladderPts=0)
        await bot.edit_message_text("Вы успешно вступили в ладдер. Текущие очки обнулены", call.message.chat.id, call.message.message_id)

async def ladderTop_(call, user):
    ladder = await db.Ladders.get_or_none(id=call.data.split("_")[1]).first()
    if ladder and ladder.active==2:
        text = "Топ игроков данного ладдера:\n"
        users = await db.Users.filter(ladder=ladder.id).order_by('-ladderPts').limit(5)
        if users:
            userInTop = 0
            count = 0
            for player in users:
                count += 1
                text += f"\n{count}: {player.username} - {player.ladderPts} pts"
                if player.id == user.id: userInTop = 1
            if user.ladder and user.ladder == ladder.id and userInTop == 0:
                text += f"\n\n{user.username}: {user.ladderPts} pts"        
        else:
            text += "\nВ ладдере еще нет игроков"
    else:
        text = "Ладдер не найден"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)





async def refs(call, user):
    allRefs = await db.Users.filter(ref=user.user_id).only('username', 'donateSum')
    refs = ""
    if allRefs:
        refs += "Список ваших рефералов:\n"
        for ref in allRefs:
            profit = ref.donateSum * 0.2
            refs += f"\n{ref.username}. Доход - {profit}"
    text = f"Приглашайте друзей в Anikado и получайте 20% 💰 от их донатов!\n\nВаша ссылка для приглашения:\nhttps://t.me/Anikado_bot?start={user.user_id}\n{refs}"
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)