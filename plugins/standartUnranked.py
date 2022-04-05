
async def startGameUnrankedStandart(player1, player2):
    await db.Users.filter(id=player1.id).update(search=0, hp=50)
    await db.Users.filter(id=player2.id).update(search=0, hp=50)
    await player1.refresh_from_db()
    await player2.refresh_from_db()
    timeStat = int(time.time()) + 120
    match = await db.Matches.create(player1=player1.id, player2=player2.id, timeStat=timeStat, tournament='unranked_standart')
    inMatch[player1.id] = []
    inMatch[player2.id] = []
    startText = "Первый ход определит монетка!"
    if random.randint(0, 100) >= 50:
        startText += "\n\nВыпала решка! Первый ход за {}".format(player2.username)
        await db.Matches.filter(id=match.id).update(status=2, p1Mana=0)
    else:
        startText += "\n\nВыпал орёл! Первый ход за {}".format(player1.username)
        await db.Matches.filter(id=match.id).update(status=1, p2Mana=0)
    try:
        await bot.send_message(player1.user_id, startText)
    except:
        pass
    try:
        await bot.send_message(player2.user_id, startText)
    except:
        pass

    textForPlayer1 = """
{} ({}❤️ ⚡️{})


{} ({}❤️ ⚡️{})
    """.format(player2.username, player2.hp, match.p2Mana, player1.username, player1.hp, match.p1Mana)
    
    textForPlayer2 = """
{} ({}❤️ ⚡️{})


{} ({}❤️ ⚡️{})
    """.format(player1.username, player1.hp, match.p1Mana, player2.username, player2.hp, match.p2Mana)


    markupP1 = InlineKeyboardMarkup()
    markupP1.row_width = 2
    markupP1.add(InlineKeyboardButton('Использовать карту', callback_data="match_addCard"))
    markupP1.add(InlineKeyboardButton('Завершить ход', callback_data="match_end"))
    try: await bot.send_message(player1.user_id, textForPlayer1, reply_markup=markupP1)
    except: pass
    markupP2 = InlineKeyboardMarkup()
    markupP2.row_width = 2
    markupP2.add(InlineKeyboardButton('Использовать карту', callback_data="match_addCard"))
    markupP2.add(InlineKeyboardButton('Завершить ход', callback_data="match_end"))
    quoteRound[match.id] = []
    try:await bot.send_message(player2.user_id, textForPlayer2, reply_markup=markupP2)
    except: pass


async def calculate_win_unranked_standart(match, player1, player2, winner):
    await db.Matches.filter(id=match.id).update(winner=winner.id, status=5)
    if winner.id == player1.id:
        await db.Users.filter(id=player1.id).update(hp=50, pvpPlayed=F('pvpPlayed') + 1, pvpWins=F('pvpWins') + 1, winsD=F('winsD') + 1, playD=F('playD') + 1)
        await db.Users.filter(id=player2.id).update(hp=50, pvpPlayed=F('pvpPlayed') + 1, pvpLose=F('pvpLose') + 1, playD=F('playD') + 1)

    elif winner.id == player2.id:
        await db.Users.filter(id=player2.id).update(hp=50, pvpPlayed=F('pvpPlayed') + 1, pvpWins=F('pvpWins') + 1, winsD=F('winsD') + 1, playD=F('playD') + 1)
        await db.Users.filter(id=player1.id).update(hp=50, pvpPlayed=F('pvpPlayed') + 1, pvpLose=F('pvpLose') + 1, playD=F('playD') + 1)

    await db.Inventory.filter(idplayer=player1.id).update(nowhp=F('hp'))
    await db.Inventory.filter(idplayer=player2.id).update(nowhp=F('hp'))