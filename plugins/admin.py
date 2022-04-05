class UserStatus(StatesGroup):
    report = State()

usersToReg = {}


@dp.message_handler(commands=['ownstartgame'])
async def ownstartgame(m):
    if m.chat.id == kakushigoto:
        global gameActive
        gameActive = 0
        await bot.send_message(kakushigoto, "Начинаю перезапуск проекта...")
        users = await db.Users.filter()
        for i in users:
            usersToReg[i.user_id] = {'id': i.id, 'donateSum': i.donateSum, 'elo': i.elo, 'ref': i.ref, 'balance': i.balance, 'username': i.username}
            await db.Users.filter(id=i.id).delete()
        await bot.send_message(kakushigoto, "Подсчёты завершены, игроки удалены. Готовлюсь к рассылке...")
        await asyncio.sleep(120)
        await bot.send_message(kakushigoto, "Рассылка началась...")
        gameActive = 1
        for user in usersToReg:
            try:
                await bot.send_message(user, "⚠️В Anikado был выпущен технический патч и обновлена система регистрации - теперь каждому новому игроку будет собираться стартовая колода. Все аккаунты были удалены из системы. Ближайшие 36 часов вам гарантируется сохранение всей истории игр, суммы донатов, ID, и прочего игрового прогресса, а так же - небольшой бонус в виде готовой стартовой колоды (или же пополнение инвентаря), состоящей из карт первого сезона!\n\nДля начала игры и восстановления прогресса нажмите /start")
                print("+1")
                await asyncio.sleep(.5)
            except: print("-1")
        print("Finish!")
        await bot.send_message(kakushigoto, "Рассылка завершена. Логирую...")
        with open(f"/home/kakushigoto/cards/backup.txt", 'a', newline='') as logFile:
            logFile.write(str(usersToReg))
            logFile.close()


@dp.message_handler(commands=['teststartgame'])
async def ownstartgame(m):
    if m.chat.id == kakushigoto:
        users = await db.Users.filter(id__in=[0, 758])
        for i in users:
            usersToReg[i.user_id] = {'id': i.id, 'donateSum': i.donateSum, 'elo': i.elo, 'ref': i.ref, 'balance': i.balance, 'username': i.username}
            await db.Users.filter(id=i.id).delete()
        print("done")
        await asyncio.sleep(10)
        for user in usersToReg:
            try:
                await bot.send_message(user, "⚠️В Anikado была обновлена стартовая система регистрации. Все аккаунты были удалены из системы. Ближайшие 48 часов вам гарантируется сохранение всей истории игр, суммы донатов, а так же - небольшой бонус в виде готовой стартовой колоды (или же пополнение инвентаря), состоящей из карт первого сезона!\n\nДля начала игры и восстановления прогресса нажмите /start")
                print("+1")
            except: print("-1")
        with open(f"/home/kakushigoto/cards/backup.txt", 'a', newline='') as logFile:
            logFile.write(str(usersToReg))
            logFile.close()
        print("Finish!")




@dp.message_handler(commands=['admin'])
async def ownpanel(m):
    if m.chat.id == kakushigoto:
        search = await db.System.get(name='search')
        if search.value == 0: search = 'Выключен'
        else: search = 'Включен'
        searching = await db.Users.filter(~Q(search=0)).only('id').count()
        playing = await db.Matches.filter(~Q(status=5)).only('id').count()
        lastTime = int(time.time()) - 86400
        matchesdaily = await db.Matches.filter(timeStat__gte=lastTime).count()
        playing *= 2
        text = """
Поиск {}
Ищет игру {}
Играют {}
Сыграно за сутки {} игр
        """.format(search, searching, playing, matchesdaily)

        games = await db.Matches.filter(~Q(status=5))
        if games:
            text += "\n\n\nТекущие игры:\n"
            for game in games:
                watching = await db.Users.filter(akTV=game.id).count()
                player1 = await db.Users.get(id=game.player1)
                player2 = await db.Users.get(id=game.player2)
                if game.tournament == 'matchmaking': gameType = "Ranked"
                elif game.tournament == 'unranked_standart': gameType = "Unranked Стандарт"
                elif game.tournament == 'unranked_short': gameType = "Unranked Короткая"
                elif game.tournament == 'unranked_war': gameType = "Unranked Война колод"
                text += "\n[{}] {} vs {} /akTV_{} (Зрителей: {})".format(gameType, player1.username, player2.username, game.id, watching)
        else:
            text += "\nК сожалению, сейчас нет игр..."



        await m.answer(text)

@dp.message_handler(commands=['getuser'])
async def getuser(m):
    if m.from_user.id == kakushigoto:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
        else:
            user_id = m.text.replace("/getuser ", "", 1)
        user = await db.Users.get_or_none(username=user_id).first()
        if not user:
            user = await db.Users.exists(id=user_id)
            if user:
                user = await db.Users.get(id=user_id).first()
            else:
                user = await db.Users.exists(user_id=user_id)
                if user:
                    user = await db.Users.get(user_id=user_id).first()
                else:
                    await m.answer("Игрока не существует")
                    return
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
            """.format(user.username, user.balance, user.elo, league, pvpPlayed, pvpWins, pvpLose, user.id)
        try:
            await bot.send_chat_action(user.user_id, 'typing')
            text += "\nValid ✅"
        except:
            text += "\nValid ❌"

        await bot.send_message(m.chat.id, text)



@dp.message_handler(commands=['ownsearch'])
async def ownsearch(m):
    if m.chat.id == kakushigoto:
        search = await db.System.get(name='search')
        if search.value == 0: await db.System.filter(name='search').update(value=1)
        else: await db.System.filter(name='search').update(value=0)
        await m.answer("Done")


@dp.message_handler(commands=['dstats'])
async def dstats(m):
    if m.chat.id == kakushigoto:
        text = ""
        donatesum = 0
        donates = await db.Users.all().order_by('-donateSum')
        for i in donates:
            donatesum += i.donateSum
        text += "Донатов на {} RUB".format(donatesum)
        topdons = await db.Users.all().order_by('-donateSum').limit(30)
        text += "\n\n\nТоп донатеров:"
        for i in topdons:
            text += "\n{} - {} RUB".format(i.username, i.donateSum)
        await bot.send_message(kakushigoto, text)


@dp.message_handler(commands=['notification'])
async def ownnotification(m):
    if m.from_user.id == kakushigoto:
        count = 0
        success = 0
        text = m.text.replace("/notification ", "", 1)
        text += "\n\n\nПодписывайся на новостной канал чтобы быть в курсе всех обновлений! @Anikado_news"
        users = await db.Users.all()
        for z in users:
            try:
                gg = await bot.get_chat_member(-1001567421100, int(z.user_id))
                if gg.status != 'left': pass
                else:
                    try:
                        await bot.send_message(z.user_id, text, disable_notification=True)
                        success += 1
                    except:
                        pass
                    count += 1
                    print("+1")
            except:
                print('error')
        await m.reply("Рассылка завершена. Письмо получили {}/{} игроков".format(success, count))




@dp.message_handler(commands=['report'])
async def report(m):
    user = await db.Users.exists(user_id=m.from_user.id)
    if user:
        user = await db.Users.get(user_id=m.from_user.id)
        if user and user.ban == 1:
            await profile(m, user)
            return
        if m.from_user.id == m.chat.id:
            await bot.send_message(m.chat.id, "Хорошо! Напишите, что хотите сообщить администрации.")
            await UserStatus.report.set()
    else:
        await start(m)

@dp.message_handler(lambda m: m.chat.id == m.from_user.id, state=UserStatus.report, content_types=types.ContentTypes.ANY)
async def report1(m, state=FSMContext):
    await state.finish()
    if m.chat.id == m.from_user.id:
        try:
            user = await db.Users.get(user_id=m.from_user.id)
            if user and user.ban != 1:
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                await bot.send_message(devChat, "Pепорт от {} , {}\n".format(m.from_user.id, user.username), reply_markup=markup)
                await bot.forward_message(devChat, m.from_user.id, m.message_id)
                await bot.send_message(m.chat.id, "Сообщение отправлено. Спасибо!")
            elif user.ban == 1:
                await bot.send_message(m.chat.id, "Ошибка доступа.")
                return
        except:
            await bot.send_message(devChat, "Pепорт от {}, {}\n{}".format(m.from_user.first_name, m.from_user.id, m.text))
            await bot.send_message(m.chat.id, "Возникла какая-то ошибка, но мы постарались отправить ваш репорт! Пожалуйста, подождите.")
@dp.message_handler(commands=['answer'])
async def answer(m):
    if str(m.from_user.id) == kakushigoto or m.chat.id == devChat:
        try:
            text = m.text.replace("/answer ", "", 1)
            __user_id = m.reply_to_message.text.replace("Pепорт от ", "", 1)
            _user_id = __user_id.split(" ")
            user_id = _user_id[0]
            if m.from_user.id == kakushigoto:
                await bot.send_message(user_id, "⚠️На ваше сообщение пришёл ответ от разработчика!⚠️\n{}".format(text))
            else:
                await bot.send_message(user_id, "⚠️На ваше сообщение пришёл ответ от администратора!⚠️\n{}".format(text))
            await bot.edit_message_text(__user_id, m.chat.id, m.reply_to_message.message_id)
            await bot.send_message(m.chat.id, "Запрос закрыт")
        except:
            await bot.send_message(m.chat.id, "Ошибка")

