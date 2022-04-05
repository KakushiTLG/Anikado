import sys
__ver__ = "1.0"
gameActive = 1
_buzyUsers = {}
__buzyUsers = {} # antiflood
import traceback
@dp.errors_handler(exception=Exception)
async def error_cant_parse(update: types.Update, error):
    if error.__class__.__name__ == 'RetryAfter':
        if "callback_query" in update:
            try:
                await bot.answer_callback_query(callback_query_id=update.callback_query.id, show_alert=True, text="Бум-бах-трах!\n{}".format(error))
                return
            except:
                return
    elif error.__class__.__name__ == 'MessageToDeleteNotFound' or error.__class__.__name__ == 'MessageNotModified' or error.__class__.__name__ == 'MessageToEditNotFound' or error.__class__.__name__ == 'InvalidQueryID':
        pass
    else:
        tb1 = sys.exc_info()[1]
        tb = sys.exc_info()[2]
        tbinfo = str(traceback.format_exc())
        await bot.send_message(702528084, f'traceback [{tbinfo}]\n\n\nerror [{error}]\n\nerror class [{error.__class__}]\n\n[{error.__class__.__name__}]\n\nupdate [{update}]')

        return True

async def checker(m):
    user = await db.Users.get_or_none(user_id=m.from_user.id).first()
    if user:
        await db.Users.filter(user_id=m.from_user.id).update(sleepPlayer=int(time.time() + 3600))
        success = True
    else:
        await start(m)
        success = False
        user = None
    return success, user


antiflood = {}
boyaraUsers = {}
testers = ['702528084']
@dp.message_handler(content_types=["text"])
async def texthand(m):
    try:
        await dp.throttle(str(m.from_user.id), rate=1)
    except exceptions.Throttled:
        return

    if gameActive == 0 and str(m.from_user.id) not in testers and m.chat.id == m.from_user.id:
        await bot.send_message(m.chat.id, "🚧Технические работы. В скором времени всё, вероятно, заработает...")
        return

    return await bot.send_message(m.chat.id, "К сожалению, проект Anikado закрыт. Возможно, когда-то он и оживёт вновь, а пока можете сыграть в другие проекты от FDU - @Operation2222_bot или @TowerOfHeaven_bot")

    if m.chat.id == m.from_user.id:
        success, user = await checker(m)
        if success == True:
            if not user:
                user = await db.Users.get_or_none(user_id=m.from_user.id).first()
                if not user:
                    await start(m)
            if user.ban != 1: pass
            else:
                await profile(m, user)
                return
            if m.text.startswith("/start"):
                await start(m)
            elif m.text.startswith('/profile'):
                await profile(m, user)
            elif m.text.startswith('/inventory'):
                await inventory(m, user)
            elif m.text.startswith('/pool'):
                await pool(m, user)
            elif m.text.startswith('/view_'):
                await view_(m, user)
            elif m.text.startswith('/specialBox'):
                await specialBox(m, user)
            elif m.text.startswith('/boxes'):
                await boxes(m, user)
            elif m.text.startswith('/globalView_'):
                await globalView_(m, user)
            elif m.text.startswith('/search'):
                await search(m, user)
            elif m.text.startswith('/donate'):
                await donate(m)
            elif m.text.startswith('/akTV_'):
                await akTV_(m, user)
            elif m.text.startswith('/ladder_'):
                await ladder_(m, user)
            elif m.text == 'Профиль': await profile(m, user)
            elif m.text == 'Инвентарь': await inventory(m, user)
            elif m.text == 'Колода': await pool(m, user)
            elif m.text == 'Боксы': await boxes(m, user)
            elif m.text == 'Поиск': await search(m, user)
            elif m.text == 'Таверна': await tavern(m, user)
            elif m.text == '/cancel': await cancel(m, user)

            # Касается обучения
            elif m.text == 'Пройти обучение': await start_1(m, user)
            elif m.text == 'Перейти к картам': await start_2(m, user)
            elif m.text == 'Отказаться от обучения': await start_start(m, user)


async def waiterTest(call):
    if __buzyUsers and call.from_user.id in __buzyUsers:
        if __buzyUsers[call.from_user.id] == 'stopped':
            passing = False
            return passing
        if __buzyUsers and call.from_user.id in __buzyUsers and __buzyUsers[call.from_user.id] > 0:
            print("Stopped {}".format(call.from_user.username))
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Ожидаем окончания предыдущего действия...")                
            count = 0
            while __buzyUsers[call.from_user.id] != 0:
                count += 1
                if count >= 20:
                    __buzyUsers[call.from_user.id] = 0
                await asyncio.sleep(0.2)
            print("Passed {}".format(call.from_user.username))
            passing = True
        elif __buzyUsers[call.from_user.id] > 10:
            print("Full stopped {}".format(call.from_user.username))
            passing = False
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Действие отменено - флуд-контроль. Попробуйте через минуту.")                
            try:
                await dp.throttle(str(call.from_user.id), rate=60)
            except exceptions.Throttled:
                return
        else:
            passing = True
    else:
        print("Already passed {}".format(call.from_user.username))
        passing = True
        __buzyUsers[int(call.from_user.id)] = 0
    return passing

@dp.callback_query_handler(lambda call: True)
async def callhand(call):
    try:
        await dp.throttle(str(call.from_user.id), rate=0.5)
    except exceptions.Throttled:
        return
    if gameActive == 0 and str(call.from_user.id) not in testers and call.message.chat.id == call.from_user.id:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🚧Технические работы")                
        return

    return await bot.send_message(call.message.chat.id, "К сожалению, проект Anikado закрыт и более не будет обновляться (https://t.me/Anikado_news/32). Можете сыграть в другие проекты от FDU - @Operation2222_bot или @TowerOfHeaven_bot")


    passing = await waiterTest(call)
    if not passing or passing != True:
        return
    user = await db.Users.get(user_id=call.from_user.id).first()
    if user.ban != 1:
        await db.Users.filter(id=user.id).update(sleepPlayer=int(time.time() + 600))
        await user.refresh_from_db(fields=['sleepPlayer'])
        d = call.data
        __buzyUsers[call.from_user.id] += 1
        if d.startswith('match'): await match(call, user)
        elif d.startswith('addCard_'): await addCard_(call, user)
        elif d.startswith('top_league'): await top_league(call, user)
        elif d.startswith('boxes'): await boxes(call, user)
        elif d.startswith('daily'): await dailyStats(call, user)
        elif d.startswith('search_'): await search_(call, user)
        elif d.startswith('akTv'): await akTv(call, user)
        elif d.startswith('premium'): await premium(call, user)
        elif d.startswith('prem_buy'): await prem_buy(call, user)
        elif d.startswith('ladders'): await ladders(call, user)
        elif d.startswith('ladderLeave_'): await ladderLeave_(call, user)
        elif d.startswith('ladderJoin_'): await ladderJoin_(call, user)
        elif d.startswith('ladderTop_'): await ladderTop_(call, user)
        elif d.startswith('createLadder'): await createLadder(call, user)
        elif d.startswith('getBonusPrem'): await getBonusPrem(call, user)
        elif d.startswith('refs'): await refs(call, user)
        await asyncio.sleep(0.2)
        __buzyUsers[call.from_user.id] -= 1
    else:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Действие отменено. Ошибка доступа.")                
    try:
        await call.answer()
    except:
        pass

@dp.message_handler(content_types=['new_chat_members'])
async def checkfrak(m):
    user = await db.Users.exists(user_id=m.from_user.id)
    if user:
        user = await db.Users.get(user_id=m.from_user.id)
        if m.chat.id == -1001651650232: # Подставить айди группы
            user = await db.Users.exists(user_id=m.from_user.id)
            if user:
                user = await db.Users.get(user_id=m.from_user.id)
                if user.ban == 0:
                    user.balance += 50
                    user.ban = 2
                    await user.save()
                    await bot.send_message(user.user_id, "Вам было зачислено 50💰 за вступление в группу!")
    else:
        await bot.kick_chat_member(m.chat.id, m.from_user.id)
        await bot.delete_message(m.chat.id, m.message_id)
