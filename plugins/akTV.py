async def akTv(call, user):
    if user.premium > 0:
        games = await db.Matches.filter(~Q(status=5))
        text = "Anikado TV - следите за текущими играми в режиме реального времени."
        if games:
            text += "\nТекущие игры:\n"
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
    else:
        text = "Anikado TV - следите за текущими играми в режиме реального времени.\n\nК сожалению, функция доступна только для Premium-игроков. Подробнее о Premium-статусе можно узнать в Таверне."
    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)


async def akTV_(m, user):
    result = m.text.replace('/akTV_', '', 1).replace('@Anikado_bot', '', 1)
    if user.premium > 0:
        getMatch = await db.Matches.get_or_none(~Q(status=5), id=result).first()
        if getMatch:
            await db.Users.filter(id=user.id).update(akTV=getMatch.id)
            player1 = await db.Users.get(id=getMatch.player1)
            player2 = await db.Users.get(id=getMatch.player2)
            await m.answer("Включено отслеживание партии {} vs {}. Если вы захотите отключить отслеживание, воспользуйтесь командой /cancel".format(player1.username, player2.username))
        else:
            await m.answer("Игра закончена либо еще не началась.")
    else:
        await m.answer("Anikado TV - следите за текущими играми в режиме реального времени.\n\nК сожалению, функция доступна только для Premium-игроков. Подробнее о Premium-статусе можно узнать в Таверне.")
async def cancel(m, user):
    await db.Users.filter(id=user.id).update(akTV=0)
    await m.answer("Отслеживание остановлено.")

async def watcher(match, text):
    watchers = await db.Users.filter(akTV=match.id)
    for user in watchers:
        try:
            await bot.send_message(user.user_id, text)
            await asyncio.sleep(.5)
        except:
            await db.Users.filter(id=user.id).update(akTV=0)