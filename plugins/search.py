async def search(m, user):
    checkBattles = await db.Matches.exists(Q(player1=user.id) | Q(player2=user.id), ~Q(status=5))
    if checkBattles: return await m.answer("У вас уже есть активная игра, необходимо сначала закончить с ней.")
    if user.search == 0:
        items = await db.Inventory.exists(idplayer=user.id, status=2)
        if not items: return await m.answer("Заполните колоду через инвентарь, без колоды особо не наиграешься...")
        search = await db.System.get(name='search')
        if search.value == 0: return await m.answer("Ведутся технические работы. Скоро всё заработает!")
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        searching = await db.Users.filter(search=1).only('id').count()
        markup.add(InlineKeyboardButton('Стандартная ranked (🔍: {})'.format(searching), callback_data="search_standart"))
        searching = await db.Users.filter(search=2).only('id').count()
        markup.add(InlineKeyboardButton('Стандартная unranked (🔍: {})'.format(searching), callback_data="search_standartUnranked"))
        searching = await db.Users.filter(search=3).only('id').count()
        markup.add(InlineKeyboardButton('Короткая unranked (🔍: {})'.format(searching), callback_data="search_shortUnranked"))
        searching = await db.Users.filter(search=4).only('id').count()
        markup.add(InlineKeyboardButton('Война колод unranked (🔍: {})'.format(searching), callback_data="search_warUnranked"))
        text = "Выберите режим, в котором хотите сыграть:\n\nСтандартная ranked - у каждого игрока на старте по 1⚡️, 50❤️. Результаты игры влияют на рейтинг и место в лиге. Для тех, кто готов разрывать топы."
        text += "\n\nСтандартная unranked - у каждого игрока на старте по 1⚡️, 50❤️. Результаты игры не влияют на рейтинг и место в лиге. Для тех, кто хочет попрактиковаться."
        text += "\n\nКороткая unranked - у каждого игрока на старте по 1⚡️, 25❤️. Результаты игры не влияют на рейтинг и место в лиге. Для тех, кто не имеет достаточно времени на полную партию."
        text += "\n\nВойна колод unranked - у каждого игрока на старте по 15⚡️, 50❤️. Результаты игры не влияют на рейтинг и место в лиге. Устройте настоящую зарубу!"
        await m.answer(text, reply_markup=markup)
    else:
        await db.Users.filter(id=user.id).update(search=0)
        await m.answer("Поиск остановлен. Для возобновления, используйте кнопку поиска")



async def search_(call, user):
    
    checkBattles = await db.Matches.exists(Q(player1=user.id) | Q(player2=user.id), ~Q(status=5))
    if checkBattles: return await bot.send_message(call.message.chat.id,"У вас уже есть активная игра, необходимо сначала закончить с ней.")

    await db.Inventory.filter(idplayer=user.id).update(nowhp=F('hp'))
    

    if call.data.split("_")[1] == 'standart':
        searching = await db.Users.filter(~Q(search=0)).only('id').count()
        playing = await db.Matches.filter(~Q(status=5)).only('id').count()
        playing *= 2
        searching += 1
        await bot.edit_message_text("Вы начали поиск игры в режиме Ranked. Если вам надоест ждать, повторно нажмите кнопку поиска\n\n🔍Всего в поиске: {}\n🎲В партии: {}\n✴️ELO: {}".format(searching, playing, user.elo), call.message.chat.id, call.message.message_id)
        rand = random.randint(3, 15)
        await db.Users.filter(id=user.id).update(search=1)
        await asyncio.sleep(rand)
        await user.refresh_from_db()
        if user.search != 1: return
        checkOthers = await db.Users.filter(~Q(id=user.id), search=1, league=user.league).only('id')
        if checkOthers:
            allPlayers = []
            for other in checkOthers:
                allPlayers.append(other.id)
            tries = 5
            while tries > 0:
                tries -= 1
                randomedEnemy = random.choice(allPlayers)
                enemy = await db.Users.get(id=randomedEnemy).first()
                checkBattles = await db.Matches.exists(Q(player1=enemy.id) | Q(player2=enemy.id), ~Q(status=5))
                if not checkBattles:
                    try:
                        await bot.send_message(enemy.user_id, "Партия найдена! \nСражение {} vs {}!".format(user.username, enemy.username))
                        await bot.send_message(user.user_id, "Партия найдена! \nСражение {} vs {}!".format(user.username, enemy.username))
                        return await startGame(user, enemy)
                    except:
                        pass
    

    elif call.data.split("_")[1] == 'standartUnranked':
        searching = await db.Users.filter(~Q(search=0)).only('id').count()
        playing = await db.Matches.filter(~Q(status=5)).only('id').count()
        playing *= 2
        searching += 1
        await bot.edit_message_text("Вы начали поиск игры в режиме Unranked. Если вам надоест ждать, повторно нажмите кнопку поиска\n\n🔍Всего в поиске: {}\n🎲В партии: {}\n✴️ELO: {}".format(searching, playing, user.elo), call.message.chat.id, call.message.message_id)
        rand = random.randint(3, 15)
        await db.Users.filter(id=user.id).update(search=2)
        await asyncio.sleep(rand)
        await user.refresh_from_db()
        if user.search != 2: return
        checkOthers = await db.Users.filter(~Q(id=user.id), search=2).only('id')
        if checkOthers:
            allPlayers = []
            for other in checkOthers:
                allPlayers.append(other.id)
            tries = 5
            while tries > 0:
                tries -= 1
                randomedEnemy = random.choice(allPlayers)
                enemy = await db.Users.get(id=randomedEnemy).first()
                checkBattles = await db.Matches.exists(Q(player1=enemy.id) | Q(player2=enemy.id), ~Q(status=5))
                if not checkBattles:
                    try:
                        await bot.send_message(enemy.user_id, "Партия найдена! \nСражение {} vs {}!".format(user.username, enemy.username))
                        await bot.send_message(user.user_id, "Партия найдена! \nСражение {} vs {}!".format(user.username, enemy.username))
                        return await startGameUnrankedStandart(user, enemy)
                    except:
                        pass
    

    elif call.data.split("_")[1] == 'shortUnranked':
        searching = await db.Users.filter(~Q(search=0)).only('id').count()
        playing = await db.Matches.filter(~Q(status=5)).only('id').count()
        playing *= 2
        searching += 1
        await bot.edit_message_text("Вы начали поиск игры в режиме Короткая Unranked. Если вам надоест ждать, повторно нажмите кнопку поиска\n\n🔍Всего в поиске: {}\n🎲В партии: {}\n✴️ELO: {}".format(searching, playing, user.elo), call.message.chat.id, call.message.message_id)
        rand = random.randint(3, 15)
        await db.Users.filter(id=user.id).update(search=3)
        await asyncio.sleep(rand)
        await user.refresh_from_db()
        if user.search != 3: return
        checkOthers = await db.Users.filter(~Q(id=user.id), search=3).only('id')
        if checkOthers:
            allPlayers = []
            for other in checkOthers:
                allPlayers.append(other.id)
            tries = 5
            while tries > 0:
                tries -= 1
                randomedEnemy = random.choice(allPlayers)
                enemy = await db.Users.get(id=randomedEnemy).first()
                checkBattles = await db.Matches.exists(Q(player1=enemy.id) | Q(player2=enemy.id), ~Q(status=5))
                if not checkBattles:
                    try:
                        await bot.send_message(enemy.user_id, "Партия найдена! \nСражение {} vs {}!".format(user.username, enemy.username))
                        await bot.send_message(user.user_id, "Партия найдена! \nСражение {} vs {}!".format(user.username, enemy.username))
                        return await startGameUnrankedShort(user, enemy)
                    except:
                        pass
    

    elif call.data.split("_")[1] == 'warUnranked':
        searching = await db.Users.filter(~Q(search=0)).only('id').count()
        playing = await db.Matches.filter(~Q(status=5)).only('id').count()
        playing *= 2
        searching += 1
        await bot.edit_message_text("Вы начали поиск игры в режиме Война колод Unranked. Если вам надоест ждать, повторно нажмите кнопку поиска\n\n🔍Всего в поиске: {}\n🎲В партии: {}\n✴️ELO: {}".format(searching, playing, user.elo), call.message.chat.id, call.message.message_id)
        rand = random.randint(3, 15)
        await db.Users.filter(id=user.id).update(search=4)
        await asyncio.sleep(rand)
        await user.refresh_from_db()
        if user.search != 4: return
        checkOthers = await db.Users.filter(~Q(id=user.id), search=4).only('id')
        if checkOthers:
            allPlayers = []
            for other in checkOthers:
                allPlayers.append(other.id)
            tries = 5
            while tries > 0:
                tries -= 1
                randomedEnemy = random.choice(allPlayers)
                enemy = await db.Users.get(id=randomedEnemy).first()
                checkBattles = await db.Matches.exists(Q(player1=enemy.id) | Q(player2=enemy.id), ~Q(status=5))
                if not checkBattles:
                    try:
                        await bot.send_message(enemy.user_id, "Партия найдена! \nСражение {} vs {}!".format(user.username, enemy.username))
                        await bot.send_message(user.user_id, "Партия найдена! \nСражение {} vs {}!".format(user.username, enemy.username))
                        return await startGameUnrankedWar(user, enemy)
                    except:
                        pass
