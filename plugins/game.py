inMatch = {}
quoteRound = {}

async def startGame(player1, player2):
    await db.Users.filter(id=player1.id).update(search=0, hp=50)
    await db.Users.filter(id=player2.id).update(search=0, hp=50)
    await player1.refresh_from_db()
    await player2.refresh_from_db()
    timeStat = int(time.time()) + 180
    match = await db.Matches.create(player1=player1.id, player2=player2.id, timeStat=timeStat)
    inMatch[player1.id] = []
    inMatch[player2.id] = []
    if int(player1.elo * 0.1) == int(player2.elo * 0.1):
        startText = "Так как матч равный, первый ход определит монетка!"
        if random.randint(0, 100) >= 50:
            startText += "\n\nВыпала решка! Первый ход за {}".format(player2.username)
            await db.Matches.filter(id=match.id).update(status=2, p1Mana=0)
        else:
            startText += "\n\nВыпал орёл! Первый ход за {}".format(player1.username)
            await db.Matches.filter(id=match.id).update(status=1, p2Mana=0)
    else:
        if player1.elo > player2.elo:
            startText = "По предварительной оценке, {} является фаворитом матча, а значит первый ход достаётся {}!".format(player1.username, player2.username)
            await db.Matches.filter(id=match.id).update(status=2, p1Mana=0)
        else:
            startText = "По предварительной оценке, {} является фаворитом матча, а значит первый ход достаётся {}!".format(player2.username, player1.username)
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

    VS

{} ({}❤️ ⚡️{})
    """.format(player2.username, player2.hp, match.p2Mana, player1.username, player1.hp, match.p1Mana)
    
    textForPlayer2 = """
{} ({}❤️ ⚡️{})

    VS

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
    await logger.write(match, 'system', startText)
    await logger.write(match, 'system', textForPlayer1)

async def match(call, user):
    match = await db.Matches.get_or_none(Q(player1=user.id) | Q(player2=user.id), ~Q(status=5))
    if not match: return await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Матч завершен либо еще не начался.")
    player1 = await db.Users.get(id=match.player1).first()
    player2 = await db.Users.get(id=match.player2).first()
    if match.status == 1 and user.id == player1.id or match.status == 2 and user.id == player2.id: pass
    elif match.status != 1 and match.status != 2:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Матч завершен либо еще не начался.")
        return
    else:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Сейчас идёт ход противника.")
        return
    timeNow = int(time.time())
    if call.data.split("_")[1] == "view":
        card1p2 = await db.Inventory.get_or_none(id=match.p2hero1).first()
        card2p2 = await db.Inventory.get_or_none(id=match.p2hero2).first()
        card3p2 = await db.Inventory.get_or_none(id=match.p2hero3).first()
        card4p2 = await db.Inventory.get_or_none(id=match.p2hero4).first()
        card5p2 = await db.Inventory.get_or_none(id=match.p2hero5).first()
        if card1p2:
            if card1p2.type == 'Охотник': ct1 = "🗡"
            elif card1p2.type == 'Защитник': ct1 = "🛡"
            elif card1p2.type == 'Маг': ct1 = '🔮'
            elif card1p2.type == 'Особый': ct1 = '🌟'
            infoCard1p2 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct1, card1p2.name, card1p2.nowhp, card1p2.atk, card1p2.idHero)
        else: infoCard1p2 = ""
        if card2p2:
            if card2p2.type == 'Охотник': ct2 = "🗡"
            elif card2p2.type == 'Защитник': ct2 = "🛡"
            elif card2p2.type == 'Маг': ct2 = '🔮'
            elif card2p2.type == 'Особый': ct2 = '🌟'
            infoCard2p2 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct2, card2p2.name, card2p2.nowhp, card2p2.atk, card2p2.idHero)
        else: infoCard2p2 = ""
        if card3p2:
            if card3p2.type == 'Охотник': ct3 = "🗡"
            elif card3p2.type == 'Защитник': ct3 = "🛡"
            elif card3p2.type == 'Маг': ct3 = '🔮'
            elif card3p2.type == 'Особый': ct3 = '🌟'
            infoCard3p2 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct3, card3p2.name, card3p2.nowhp, card3p2.atk, card3p2.idHero)
        else: infoCard3p2 = ""
        if card4p2:
            if card4p2.type == 'Охотник': ct4 = "🗡"
            elif card4p2.type == 'Защитник': ct4 = "🛡"
            elif card4p2.type == 'Маг': ct4 = '🔮'
            elif card4p2.type == 'Особый': ct4 = '🌟'
            infoCard4p2 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct4, card4p2.name, card4p2.nowhp, card4p2.atk, card4p2.idHero)
        else: infoCard4p2 = ""
        if card5p2:
            if card5p2.type == 'Охотник': ct5 = "🗡"
            elif card5p2.type == 'Защитник': ct5 = "🛡"
            elif card5p2.type == 'Маг': ct5 = '🔮'
            elif card5p2.type == 'Особый': ct5 = '🌟'
            infoCard5p2 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct5, card5p2.name, card5p2.nowhp, card5p2.atk, card5p2.idHero)
        else: infoCard5p2 = ""

        card1p1 = await db.Inventory.get_or_none(id=match.p1hero1).first()
        card2p1 = await db.Inventory.get_or_none(id=match.p1hero2).first()
        card3p1 = await db.Inventory.get_or_none(id=match.p1hero3).first()
        card4p1 = await db.Inventory.get_or_none(id=match.p1hero4).first()
        card5p1 = await db.Inventory.get_or_none(id=match.p1hero5).first()
        if card1p1:
            if card1p1.type == 'Охотник': ct1 = "🗡"
            elif card1p1.type == 'Защитник': ct1 = "🛡"
            elif card1p1.type == 'Маг': ct1 = '🔮'
            elif card1p1.type == 'Особый': ct1 = '🌟'
            infoCard1p1 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct1, card1p1.name, card1p1.nowhp, card1p1.atk, card1p1.idHero)
        else: infoCard1p1 = ""
        if card2p1:
            if card2p1.type == 'Охотник': ct2 = "🗡"
            elif card2p1.type == 'Защитник': ct2 = "🛡"
            elif card2p1.type == 'Маг': ct2 = '🔮'
            elif card2p1.type == 'Особый': ct2 = '🌟'
            infoCard2p1 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct2, card2p1.name, card2p1.nowhp, card2p1.atk, card2p1.idHero)
        else: infoCard2p1 = ""
        if card3p1:
            if card3p1.type == 'Охотник': ct3 = "🗡"
            elif card3p1.type == 'Защитник': ct3 = "🛡"
            elif card3p1.type == 'Маг': ct3 = '🔮'
            elif card3p1.type == 'Особый': ct3 = '🌟'
            infoCard3p1 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct3, card3p1.name, card3p1.nowhp, card3p1.atk, card3p1.idHero)
        else: infoCard3p1 = ""
        if card4p1:
            if card4p1.type == 'Охотник': ct4 = "🗡"
            elif card4p1.type == 'Защитник': ct4 = "🛡"
            elif card4p1.type == 'Маг': ct4 = '🔮'
            elif card4p1.type == 'Особый': ct4 = '🌟'
            infoCard4p1 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct4, card4p1.name, card4p1.nowhp, card4p1.atk, card4p1.idHero)
        else: infoCard4p1 = ""
        if card5p1:
            if card5p1.type == 'Охотник': ct5 = "🗡"
            elif card5p1.type == 'Защитник': ct5 = "🛡"
            elif card5p1.type == 'Маг': ct5 = '🔮'
            elif card5p1.type == 'Особый': ct5 = '🌟'
            infoCard5p1 = "\n{}{} ({}❤️ {}💢) - /globalView_{}".format(ct5, card5p1.name, card5p1.nowhp, card5p1.atk, card5p1.idHero)
        else: infoCard5p1 = ""


        textForPlayer1 = """
{} ({}❤️ ⚡️{})

    Герои:
    {}{}{}{}{}


{} ({}❤️ ⚡️{})

    Герои:
    {}{}{}{}{}

        """.format(player2.username, player2.hp, match.p2Mana, infoCard1p2, infoCard2p2, infoCard3p2, infoCard4p2, infoCard5p2, player1.username, player1.hp, match.p1Mana, infoCard1p1, infoCard2p1, infoCard3p1, infoCard4p1, infoCard5p1)
        
        textForPlayer2 = """
{} ({}❤️ ⚡️{})

    Герои:
    {}{}{}{}{}


{} ({}❤️ ⚡️{})

    Герои:
    {}{}{}{}{}

        """.format(player1.username, player1.hp, match.p1Mana, infoCard1p1, infoCard2p1, infoCard3p1, infoCard4p1, infoCard5p1, player2.username, player2.hp, match.p2Mana, infoCard1p2, infoCard2p2, infoCard3p2, infoCard4p2, infoCard5p2)
        
        markupP1 = InlineKeyboardMarkup()
        markupP1.row_width = 2
        markupP1.add(InlineKeyboardButton('Использовать карту', callback_data="match_addCard"))
        card1 = await db.Inventory.get_or_none(id=match.p1hero1).first()
        card2 = await db.Inventory.get_or_none(id=match.p1hero2).first()
        card3 = await db.Inventory.get_or_none(id=match.p1hero3).first()
        card4 = await db.Inventory.get_or_none(id=match.p1hero4).first()
        card5 = await db.Inventory.get_or_none(id=match.p1hero5).first()
        if card1 and card1.id not in quoteRound[match.id]: markupP1.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card1p1.rare, card1p1.name, card1p1.type), callback_data='match_card_1'))
        if card2 and card2.id not in quoteRound[match.id]: markupP1.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card2p1.rare, card2p1.name, card2p1.type), callback_data='match_card_2'))
        if card3 and card3.id not in quoteRound[match.id]: markupP1.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card3p1.rare, card3p1.name, card3p1.type), callback_data='match_card_3'))
        if card4 and card4.id not in quoteRound[match.id]: markupP1.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card4p1.rare, card4p1.name, card4p1.type), callback_data='match_card_4'))
        if card5 and card5.id not in quoteRound[match.id]: markupP1.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card5p1.rare, card5p1.name, card5p1.type), callback_data='match_card_5'))
        markupP1.add(InlineKeyboardButton('Завершить ход', callback_data="match_end"))
        markupP1.add(InlineKeyboardButton('Сдаться', callback_data="match_surrend"))
        try: await bot.send_message(player1.user_id, textForPlayer1, reply_markup=markupP1)
        except: pass
        markupP2 = InlineKeyboardMarkup()
        markupP2.row_width = 2
        markupP2.add(InlineKeyboardButton('Использовать карту', callback_data="match_addCard"))
        card1 = await db.Inventory.get_or_none(id=match.p2hero1).first()
        card2 = await db.Inventory.get_or_none(id=match.p2hero2).first()
        card3 = await db.Inventory.get_or_none(id=match.p2hero3).first()
        card4 = await db.Inventory.get_or_none(id=match.p2hero4).first()
        card5 = await db.Inventory.get_or_none(id=match.p2hero5).first()
        if card1 and card1.id not in quoteRound[match.id]: markupP2.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card1p2.rare, card1p2.name, card1p2.type), callback_data='match_card_1'))
        if card2 and card2.id not in quoteRound[match.id]: markupP2.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card2p2.rare, card2p2.name, card2p2.type), callback_data='match_card_2'))
        if card3 and card3.id not in quoteRound[match.id]: markupP2.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card3p2.rare, card3p2.name, card3p2.type), callback_data='match_card_3'))
        if card4 and card4.id not in quoteRound[match.id]: markupP2.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card4p2.rare, card4p2.name, card4p2.type), callback_data='match_card_4'))
        if card5 and card5.id not in quoteRound[match.id]: markupP2.add(InlineKeyboardButton('{}⭐️ {} {}'.format(card5p2.rare, card5p2.name, card5p2.type), callback_data='match_card_5'))
        markupP2.add(InlineKeyboardButton('Завершить ход', callback_data="match_end"))
        markupP2.add(InlineKeyboardButton('Сдаться', callback_data="match_surrend"))
        try: await bot.send_message(player2.user_id, textForPlayer2, reply_markup=markupP2)
        except: pass
        await watcher(match, textForPlayer2)
        await logger.write(match, 'system', textForPlayer1)
        return
    if call.data.split("_")[1] == 'end':
        if True:
            newTimeStat = int(time.time()) + 180
            if match.status == 1:
                if match.p2Mana <= 9: 
                    await db.Matches.filter(id=match.id).update(status=2, p2Mana=F('p2Mana') + 1, timeStat=newTimeStat)
                else:
                    await db.Matches.filter(id=match.id).update(status=2, timeStat=newTimeStat)
            elif match.status == 2: 
                if match.p1Mana <= 9:
                    await db.Matches.filter(id=match.id).update(status=1, p1Mana=F('p1Mana') + 1, timeStat=newTimeStat)
                else:
                    await db.Matches.filter(id=match.id).update(status=1, timeStat=newTimeStat)
            await match.refresh_from_db()
            quoteRound[match.id] = []
            try:
                if match.status == 1:
                    markup = InlineKeyboardMarkup()
                    markup.row_width = 2
                    markup.add(InlineKeyboardButton('Начать ход.', callback_data="match_view"))
                    try: await bot.send_message(player1.user_id, "{} заканчивает ход. Теперь твой черёд!".format(user.username), reply_markup=markup)
                    except: pass
                else:
                    try: await bot.send_message(player1.user_id, "{} заканчивает ход.".format(user.username))
                    except: pass
            except:
                pass
            try:
                if match.status == 2:
                    markup = InlineKeyboardMarkup()
                    markup.row_width = 2
                    markup.add(InlineKeyboardButton('Начать ход.', callback_data="match_view"))
                    try: await bot.send_message(player2.user_id, "{} заканчивает ход. Теперь твой черёд!".format(user.username), reply_markup=markup)
                    except: pass
                else:
                    try: await bot.send_message(player2.user_id, "{} заканчивает ход.".format(user.username))
                    except: pass
            except:
                pass
            text = "{} заканчивает ход".format(user.username)
            await watcher(match, text)
            await logger.write(match, user.username, text)

        return
    elif call.data.split("_")[1] == 'card':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if match.status == 1:
            if call.data.split("_")[2] == '1': card = await db.Inventory.get_or_none(id=match.p1hero1).first()
            elif call.data.split("_")[2] == '2': card = await db.Inventory.get_or_none(id=match.p1hero2).first()
            elif call.data.split("_")[2] == '3': card = await db.Inventory.get_or_none(id=match.p1hero3).first()
            elif call.data.split("_")[2] == '4': card = await db.Inventory.get_or_none(id=match.p1hero4).first()
            elif call.data.split("_")[2] == '5': card = await db.Inventory.get_or_none(id=match.p1hero5).first()
        
            if card.nowhp > 0:
                text = "\n{} {} ({}/{}❤️ 💢{})\n(/view_{}). Выбери кого атаковать".format(card.name, card.type, card.nowhp, card.hp, card.atk, card.id)
                card1 = await db.Inventory.get_or_none(id=match.p2hero1).first()
                card2 = await db.Inventory.get_or_none(id=match.p2hero2).first()
                card3 = await db.Inventory.get_or_none(id=match.p2hero3).first()
                card4 = await db.Inventory.get_or_none(id=match.p2hero4).first()
                card5 = await db.Inventory.get_or_none(id=match.p2hero5).first()
                armored = 0
                if card1 and card1.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card1.name, card1.type, card1.nowhp, card1.atk), callback_data='match_atk_{}_{}'.format(card.id, card1.id)))
                    if card1.type == 'Защитник':
                        armored = 1
                if card2 and card2.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card2.name, card2.type, card2.nowhp, card2.atk), callback_data='match_atk_{}_{}'.format(card.id, card2.id)))
                    if card2.type == 'Защитник':
                        armored = 1
                if card3 and card3.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card3.name, card3.type, card3.nowhp, card3.atk), callback_data='match_atk_{}_{}'.format(card.id, card3.id)))
                    if card3.type == 'Защитник':
                        armored = 1
                if card4 and card4.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card4.name, card4.type, card4.nowhp, card4.atk), callback_data='match_atk_{}_{}'.format(card.id, card4.id)))
                    if card4.type == 'Защитник':
                        armored = 1
                if card5 and card5.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card5.name, card5.type, card5.nowhp, card5.atk), callback_data='match_atk_{}_{}'.format(card.id, card5.id)))
                    if card5.type == 'Защитник':
                        armored = 1
                if armored == 0:
                    markup.add(InlineKeyboardButton('{} ({}❤️)'.format(player2.username, player2.hp), callback_data='match_atk_{}_player'.format(card.id)))

            else:
                text = "\n{} {} (0❤️)\n(/view_{}). Карту нужно убрать с поля".format(card.name, card.type, card.nowhp, card.id)
                markup.add(InlineKeyboardButton('Убрать карту', callback_data="match_deleteCard_{}".format(card.id)))


        elif match.status == 2:
            if call.data.split("_")[2] == '1': card = await db.Inventory.get_or_none(id=match.p2hero1).first()
            elif call.data.split("_")[2] == '2': card = await db.Inventory.get_or_none(id=match.p2hero2).first()
            elif call.data.split("_")[2] == '3': card = await db.Inventory.get_or_none(id=match.p2hero3).first()
            elif call.data.split("_")[2] == '4': card = await db.Inventory.get_or_none(id=match.p2hero4).first()
            elif call.data.split("_")[2] == '5': card = await db.Inventory.get_or_none(id=match.p2hero5).first()

            if card.nowhp > 0:
                text = "\n{} {} ({}/{}❤️ 💢{})\n(/view_{}). Выбери кого атаковать".format(card.name, card.type, card.nowhp, card.hp, card.atk, card.id)
                card1 = await db.Inventory.get_or_none(id=match.p1hero1).first()
                card2 = await db.Inventory.get_or_none(id=match.p1hero2).first()
                card3 = await db.Inventory.get_or_none(id=match.p1hero3).first()
                card4 = await db.Inventory.get_or_none(id=match.p1hero4).first()
                card5 = await db.Inventory.get_or_none(id=match.p1hero5).first()
                armored = 0
                if card1 and card1.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card1.name, card1.type, card1.nowhp, card1.atk), callback_data='match_atk_{}_{}'.format(card.id, card1.id)))
                    if card1.type == 'Защитник':
                        armored = 1
                if card2 and card2.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card2.name, card2.type, card2.nowhp, card2.atk), callback_data='match_atk_{}_{}'.format(card.id, card2.id)))
                    if card2.type == 'Защитник':
                        armored = 1
                if card3 and card3.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card3.name, card3.type, card3.nowhp, card3.atk), callback_data='match_atk_{}_{}'.format(card.id, card3.id)))
                    if card3.type == 'Защитник':
                        armored = 1
                if card4 and card4.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card4.name, card4.type, card4.nowhp, card4.atk), callback_data='match_atk_{}_{}'.format(card.id, card4.id)))
                    if card4.type == 'Защитник':
                        armored = 1
                if card5 and card5.nowhp > 0: 
                    markup.add(InlineKeyboardButton('{} {} ({}❤️ 💢{})'.format(card5.name, card5.type, card5.nowhp, card5.atk), callback_data='match_atk_{}_{}'.format(card.id, card5.id)))
                    if card5.type == 'Защитник':
                        armored = 1
                if armored == 0:
                    markup.add(InlineKeyboardButton('{} ({}❤️)'.format(player1.username, player1.hp), callback_data='match_atk_{}_player'.format(card.id)))
            else:
                text = "\n{} {} (0❤️)\n(/view_{}). Карту нужно убрать с поля".format(card.name, card.type, card.nowhp, card.id)
                markup.add(InlineKeyboardButton('Убрать карту', callback_data="match_deleteCard_{}".format(card.id)))
        
        markup.add(InlineKeyboardButton('К полю', callback_data="match_view"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif call.data.split("_")[1] == 'atk':
        attacker = await db.Inventory.get(id=call.data.split("_")[2])
        if attacker.nowhp <= 0: return await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Карта мертва, вы не можете её использовать.")
        if attacker.id in quoteRound[match.id]:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Эта карта уже сделала ход.")
            return
        if attacker.name == 'Сейбер' and attacker.rare == 4:
            if attacker.nowhp < 5: attacker.atk = 13
        quoteRound[match.id].append(attacker.id)
        defender = call.data.split("_")[3]
        if defender != 'player':
            defender = await db.Inventory.get(id=call.data.split("_")[3])
            if defender.name == 'Даркнесс' and defender.rare == 4:
                attacker.atk = int(attacker.atk * 0.8)
            
            # Daily
            if defender.nowhp - attacker.atk > 0:
                if attacker.type == 'Охотник': await db.Users.filter(id=user.id).update(dmgA=F('dmgA') + attacker.atk)
                elif attacker.type == 'Защитник': await db.Users.filter(id=user.id).update(dmgD=F('dmgD') + attacker.atk)
                elif attacker.type == 'Маг': await db.Users.filter(id=user.id).update(dmgM=F('dmgM') + attacker.atk)
                elif attacker.type == 'Особый': await db.Users.filter(id=user.id).update(dmgO=F('dmgO') + attacker.atk)

                await db.Inventory.filter(id=call.data.split("_")[3]).update(nowhp=F('nowhp') - attacker.atk)
                defender.nowhp = defender.nowhp - attacker.atk
                if defender.type == 'Охотник': defender.type = "🗡"
                elif defender.type == 'Защитник': defender.type = "🛡"
                elif defender.type == 'Маг': defender.type = '🔮'
                elif defender.type == 'Особый': defender.type = "🌟"
                if attacker.type == 'Охотник': attacker.type = "🗡"
                elif attacker.type == 'Защитник': attacker.type = "🛡"
                elif attacker.type == 'Маг': attacker.type = '🔮'
                elif attacker.type == 'Особый': attacker.type = "🌟"
                try:
                    await bot.send_message(player1.user_id, "{} {} наносит {}🗡 карте {} {}. У него остаётся {}❤️".format(attacker.type, attacker.name, attacker.atk, defender.name, defender.type, defender.nowhp))
                except:
                    pass
                try:
                    await bot.send_message(player2.user_id, "{} {} наносит {}🗡 карте {} {}. У него остаётся {}❤️".format(attacker.type, attacker.name, attacker.atk, defender.name, defender.type, defender.nowhp))
                except:
                    pass
                text = "[{}]: {} {} наносит {}🗡 карте {} {}. У него остаётся {}❤️".format(user.username, attacker.type, attacker.name, attacker.atk, defender.name, defender.type, defender.nowhp)
                await watcher(match, text)
                await logger.write(match, user.username, text)
                await defender.refresh_from_db()
                await attacker.refresh_from_db()

            else:
                if attacker.type == 'Охотник': await db.Users.filter(id=user.id).update(dmgA=F('dmgA') + defender.nowhp)
                elif attacker.type == 'Защитник': await db.Users.filter(id=user.id).update(dmgD=F('dmgD') + defender.nowhp)
                elif attacker.type == 'Маг': await db.Users.filter(id=user.id).update(dmgM=F('dmgM') + defender.nowhp)
                elif attacker.type == 'Особый': await db.Users.filter(id=user.id).update(dmgO=F('dmgO') + defender.nowhp)
                await db.Inventory.filter(id=call.data.split("_")[3]).update(nowhp=0)
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                if attacker.type == 'Охотник': attacker.type = "🗡"
                elif attacker.type == 'Защитник': attacker.type = "🛡"
                elif attacker.type == 'Маг': attacker.type = '🔮'
                elif attacker.type == 'Особый': attacker.type = "🌟"


                #SKILLS

                if attacker.name == 'Ято' and attacker.rare == 5: await db.Inventory.filter(id=attacker.id).update(nowhp=F('nowhp') + 2)


                # Daily
                if defender.type == 'Охотник': await db.Users.filter(id=user.id).update(killA=F('killA') + 1)
                elif defender.type == 'Защитник': await db.Users.filter(id=user.id).update(killD=F('killD') + 1)
                elif defender.type == 'Маг': await db.Users.filter(id=user.id).update(killM=F('killM') + 1)
                elif defender.type == 'Особый': await db.Users.filter(id=user.id).update(killO=F('killO') + 1)

                if defender.type == 'Охотник': defender.type = "🗡"
                elif defender.type == 'Защитник': defender.type = "🛡"
                elif defender.type == 'Маг': defender.type = '🔮'
                elif defender.type == 'Особый': defender.type = "🌟"
                


                try:
                    if match.status == 1:
                        markup.add(InlineKeyboardButton('Продолжить ход.', callback_data="match_view"))
                    await bot.send_message(player1.user_id, "{} {} наносит {}🗡 карте {} {}. Карта умирает.".format(attacker.type, attacker.name, attacker.atk, defender.name, defender.type), reply_markup=markup)
                except:
                    pass
                try:
                    if match.status == 2:
                        markup.add(InlineKeyboardButton('Продолжить ход.', callback_data="match_view"))
                    await bot.send_message(player2.user_id, "{} {} наносит {}🗡 карте {} {}. Карта умирает.".format(attacker.type, attacker.name, attacker.atk, defender.name, defender.type), reply_markup=markup)
                except:
                    pass
                text = "[{}]: {} {} наносит {}🗡 карте {} {}. Карта умирает.".format(user.username, attacker.type, attacker.name, attacker.atk, defender.name, defender.type)
                await watcher(match, text)
                await logger.write(match, user.username, text)
                await defender.refresh_from_db()
                await attacker.refresh_from_db()
        elif defender == 'player':
            if match.status == 1:
                defender = player2
            elif match.status == 2:
                defender = player1
            if defender.hp - attacker.atk > 0:
                await db.Users.filter(id=defender.id).update(hp=F('hp') - attacker.atk)
                defender.hp -= attacker.atk
                if attacker.type == 'Охотник': attacker.type = "🗡"
                elif attacker.type == 'Защитник': attacker.type = "🛡"
                elif attacker.type == 'Маг': attacker.type = '🔮'
                elif attacker.type == 'Особый': attacker.type = "🌟"
                try:
                    await bot.send_message(player1.user_id, "{} {} наносит {}🗡 {}. У него остаётся {}❤️".format(attacker.type, attacker.name, attacker.atk, defender.username, defender.hp))
                except:
                    pass
                try:
                    await bot.send_message(player2.user_id, "{} {} наносит {}🗡 {}. У него остаётся {}❤️".format(attacker.type, attacker.name, attacker.atk, defender.username, defender.hp))
                except:
                    pass
                text = "[{}]: {} {} наносит {}🗡 {}. У него остаётся {}❤️".format(user.username, attacker.type, attacker.name, attacker.atk, defender.username, defender.hp)
                await watcher(match, text)
                await logger.write(match, user.username, text)
                await defender.refresh_from_db()
                await attacker.refresh_from_db()
            else:
                await db.Users.filter(id=defender.id).update(hp=50)
                markup = InlineKeyboardMarkup()
                markup.row_width = 2
                if attacker.type == 'Охотник': attacker.type = "🗡"
                elif attacker.type == 'Защитник': attacker.type = "🛡"
                elif attacker.type == 'Маг': attacker.type = '🔮'
                elif attacker.type == 'Особый': attacker.type = "🌟"
                try:
                    if match.status == 1:
                        winner = player1
                        await bot.send_message(player1.user_id, "{} {} наносит {}🗡 {}. Игра закончена, победа за {}!".format(attacker.type, attacker.name, attacker.atk, defender.username, player1.username))
                    else:
                        winner = player2
                        await bot.send_message(player1.user_id, "{} {} наносит {}🗡 {}. Игра закончена, победа за {}!".format(attacker.type, attacker.name, attacker.atk, defender.username, player2.username))
                except:
                    pass
                try:
                    if match.status == 1:
                        winner = player1
                        await bot.send_message(player2.user_id, "{} {} наносит {}🗡 {}. Игра закончена, победа за {}!".format(attacker.type, attacker.name, attacker.atk, defender.username, player1.username))
                    else:
                        winner = player2
                        await bot.send_message(player2.user_id, "{} {} наносит {}🗡 {}. Игра закончена, победа за {}!".format(attacker.type, attacker.name, attacker.atk, defender.username, player2.username))
                except:
                    pass
                text = "[{}]: {} {} наносит {}🗡 {}. Игра закончена, победа за {}!".format(user.username, attacker.type, attacker.name, attacker.atk, defender.username, player2.username)
                await watcher(match, text)
                await logger.write(match, user.username, text)
                await defender.refresh_from_db()
                await attacker.refresh_from_db()
                await calculate_win(match, player1, player2, winner)
        return

    elif call.data.split("_")[1] == 'addCard':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        if match.status == 1 and user.id == match.player1:
            text = "У тебя {}⚡️\nВыбери героя, которого желаешь добавить на поле боя.\n".format(match.p1Mana)
            allHeroes = await db.Inventory.filter(idplayer=user.id, status=2)
            for hero in allHeroes:
                if hero.nowhp == hero.hp:
                    if hero.id == match.p1hero1 or hero.id == match.p1hero2 or hero.id == match.p1hero3 or hero.id == match.p1hero4 or hero.id == match.p1hero5 or hero.id in inMatch[user.id]:
                        pass
                    else:
                        if hero.type == 'Охотник': Type = "🗡"
                        elif hero.type == 'Защитник': Type = "🛡"
                        elif hero.type == 'Маг': Type = '🔮'
                        elif hero.type == 'Особый': Type = "🌟"
                        text += "\n{}⭐️ ({}⚡️) {}{} (({}❤️ 💢{})) (/view_{})".format(hero.rare, hero.rare, Type, hero.name, hero.hp, hero.atk, hero.id)
                        markup.add(InlineKeyboardButton("{}⭐️ {} {}".format(hero.rare, hero.name, hero.type), callback_data="addCard_{}".format(hero.id)))
        
        elif match.status == 2 and user.id == match.player2:
            text = "У тебя {}⚡️\nВыбери героя, которого желаешь добавить на поле боя.\n".format(match.p2Mana)
            allHeroes = await db.Inventory.filter(idplayer=user.id, status=2)
            for hero in allHeroes:
                if hero.nowhp == hero.hp:
                    if hero.id == match.p2hero1 or hero.id == match.p2hero2 or hero.id == match.p2hero3 or hero.id == match.p2hero4 or hero.id == match.p2hero5 or hero.id in inMatch[user.id]:
                        pass
                    else:
                        if hero.type == 'Охотник': Type = "🗡"
                        elif hero.type == 'Защитник': Type = "🛡"
                        elif hero.type == 'Маг': Type = '🔮'
                        elif hero.type == 'Особый': Type = "🌟"
                        text += "\n{}⭐️ ({}⚡️) {}{} (({}❤️ 💢{})) (/view_{})".format(hero.rare, hero.rare, Type, hero.name, hero.hp, hero.atk, hero.id)
                        markup.add(InlineKeyboardButton("{}⭐️ {} {}".format(hero.rare, hero.name, hero.type), callback_data="addCard_{}".format(hero.id)))

        markup.add(InlineKeyboardButton('К полю', callback_data="match_view"))
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif call.data.split("_")[1] == 'deleteCard':
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        hero = await db.Inventory.get_or_none(id=call.data.split("_")[2])
        if match.status == 1:
            if match.p1hero1 == hero.id: match.p1hero1 = None
            elif match.p1hero2 == hero.id: match.p1hero2 = None
            elif match.p1hero3 == hero.id: match.p1hero3 = None
            elif match.p1hero4 == hero.id: match.p1hero4 = None
            elif match.p1hero5 == hero.id: match.p1hero5 = None
        elif match.status == 2:
            if match.p2hero1 == hero.id: match.p2hero1 = None
            elif match.p2hero2 == hero.id: match.p2hero2 = None
            elif match.p2hero3 == hero.id: match.p2hero3 = None
            elif match.p2hero4 == hero.id: match.p2hero4 = None
            elif match.p2hero5 == hero.id: match.p2hero5 = None
        await match.save()
        try:
            await bot.send_message(player1.user_id, "Карта {} {} была убрана с поля".format(hero.name, hero.type))
        except:
            pass
        try:
            await bot.send_message(player2.user_id, "Карта {} {} была убрана с поля".format(hero.name, hero.type))
        except:
            pass
        text = "Готово!"
        markup.add(InlineKeyboardButton('Продолжить ход.', callback_data="match_view"))
        text = "[{}]: Карта {} {} была убрана с поля".format(user.username, hero.name, hero.type)
        await watcher(match, text)
        await logger.write(match, user.username, text)


    elif call.data.split("_")[1] == 'surrend':
        if match.status == 1:
            defender = player1
        elif match.status == 2:
            defender = player2
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Точно сдаться', callback_data="match_surrendYes"))
        markup.add(InlineKeyboardButton('Вернуться в игру.', callback_data="match_view"))
        text = "Вы точно хотите сдаться?"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        return
    elif call.data.split("_")[1] == 'surrendYes':
        if match.status == 1:
            defender = player1
        elif match.status == 2:
            defender = player2
        await db.Users.filter(id=player1.id).update(hp=50)
        await db.Users.filter(id=player2.id).update(hp=50)
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        try:
            if match.status == 1:
                winner = player2
                try: await bot.send_message(player1.user_id, "{} признаёт своё поражение. Игра закончена, победа за {}!".format(defender.username, winner.username))
                except: pass
            else:
                winner = player1
                try: await bot.send_message(player1.user_id, "{} признаёт своё поражение. Игра закончена, победа за {}!".format(defender.username, winner.username))
                except: pass
            text = "{} признаёт своё поражение. Игра закончена, победа за {}!".format(defender.username, winner.username)
            await watcher(match, text)
            await logger.write(match, user.username, text)
        except:
            pass
        try:
            if match.status == 1:
                winner = player2
                await bot.send_message(player2.user_id, "{} признаёт своё поражение. Игра закончена, победа за {}!".format(defender.username, winner.username))
            else:
                winner = player1
                await bot.send_message(player2.user_id, "{} признаёт своё поражение. Игра закончена, победа за {}!".format(defender.username, winner.username))
            text = "{} признаёт своё поражение. Игра закончена, победа за {}!".format(defender.username, winner.username)
        except:
            pass
        if match.tournament == 'unranked_standart': return await calculate_win_unranked_standart(match, player1, player2, winner)
        elif match.tournament == 'unranked_short': return await calculate_win_unranked_short(match, player1, player2, winner)
        elif match.tournament == 'unranked_war': return await calculate_win_unranked_war(match, player1, player2, winner)
        else: await calculate_win(match, player1, player2, winner)
        return


    await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)



async def addCard_(call, user):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    heroId = call.data.split("_")[1]
    match = await db.Matches.get_or_none(Q(player1=user.id) | Q(player2=user.id), ~Q(status=5))
    if not match: return await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Матч завершен либо еще не начался.")
    player1 = await db.Users.get(id=match.player1).first()
    player2 = await db.Users.get(id=match.player2).first()
    if match.status == 1 and user.id == player1.id or match.status == 2 and user.id == player2.id: pass
    elif match.status != 1 and match.status != 2:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Матч завершен либо еще не начался.")
        return
    else: 
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Сейчас идёт ход противника.")
        return
    hero = await db.Inventory.get(id=heroId).first()
    if hero.id in inMatch:
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Эта карта уже призывалась в партии.")
        return
    if hero.nowhp == hero.hp:
        if user.id == player1.id:
            if hero.id not in [match.p1hero1, match.p1hero2, match.p1hero3, match.p1hero4, match.p1hero5]:
                if match.p1Mana < hero.rare:
                    try: await bot.send_message(call.message.chat.id, "У тебя не хватает энергии для призыва этой карты")
                    except: pass
                    return
                if not match.p1hero1: match.p1hero1 = hero.id
                elif not match.p1hero2: match.p1hero2 = hero.id
                elif not match.p1hero3: match.p1hero3 = hero.id
                elif not match.p1hero4: match.p1hero4 = hero.id
                elif not match.p1hero5: match.p1hero5 = hero.id
                else:
                    checkHero1 = await db.Inventory.get(id=match.p1hero1)
                    if checkHero1.nowhp <= 0:
                        match.p1hero1 = hero.id
                    else:
                        checkHero2 = await db.Inventory.get(id=match.p1hero2)
                        if checkHero2.nowhp <= 0:
                            match.p1hero2 = hero.id
                        else:
                            checkHero3 = await db.Inventory.get(id=match.p1hero3)
                            if checkHero3.nowhp <= 0:
                                match.p1hero3 = hero.id 
                            else:
                                checkHero4 = await db.Inventory.get(id=match.p1hero4)
                                if checkHero4.nowhp <= 0:
                                    match.p1hero4 = hero.id 
                                else:
                                    checkHero5 = await db.Inventory.get(id=match.p1hero5)
                                    if checkHero5.nowhp <= 0 :
                                        match.p1hero5 = hero.id
                                    else:
                                        text = "У тебя нет места для вызова карты. Максимальное количество карт на поле - 5!"
                                        try: await bot.send_message(call.message.chat.id, text)
                                        except: pass
                                        return
                if match.p1Mana >= hero.rare:
                    match.p1Mana -= hero.rare
                if hero.name == 'Аято' and hero.rare == 4 and hero.type == "Маг":
                    match.p1Mana += 1
                    match.p2Mana -= 1
                elif hero.name == 'Канадэ' and hero.rare == 4 and hero.type == 'Охотник':
                    killedName = None
                    checkCard = await db.Inventory.get_or_none(id=match.p2hero1)
                    if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                        checkCard.nowhp = 0
                        killedName = checkCard.name
                    else:
                        checkCard = await db.Inventory.get_or_none(id=match.p2hero2)
                        if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                            checkCard.nowhp = 0
                            killedName = checkCard.name
                        else:
                            checkCard = await db.Inventory.get_or_none(id=match.p2hero3)
                            if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                                checkCard.nowhp = 0
                                killedName = checkCard.name
                            else:
                                checkCard = await db.Inventory.get_or_none(id=match.p2hero4)
                                if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                                    checkCard.nowhp = 0
                                    killedName = checkCard.name
                                else:
                                    checkCard = await db.Inventory.get_or_none(id=match.p2hero5)
                                    if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                                        checkCard.nowhp = 0
                                        killedName = checkCard.name
                    if killedName:
                        await checkCard.save()
                        try: await bot.send_message(player1.user_id, "Карта {} была уничтожена".format(killedName))
                        except: pass
                        try: await bot.send_message(player2.user_id, "Карта {} была уничтожена".format(killedName))
                        except: pass
                        text = "[{}]: Карта {} была уничтожена".format(user.username, killedName)
                        await watcher(match, text)
                        await logger.write(match, user.username, text)


                text = "Игроком {} на поле боя была призвана карта {} (/globalView_{})!".format(player1.username, hero.name, hero.idHero)
                await watcher(match, text)
                await logger.write(match, user.username, text)
                markup.add(InlineKeyboardButton('К полю', callback_data="match_view"))
                inMatch[user.id].append(hero.id)
                await match.save()
                await bot.edit_message_text("Призыв завершен.", call.message.chat.id, call.message.message_id, reply_markup=markup)
                if hero.name == 'Аято' and hero.rare == 4 and hero.type == "Маг":
                    try: await bot.send_message(player1.user_id, "Пришло время предать вас забвению!")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Пришло время предать вас забвению!")
                    except: pass
                elif hero.name == 'Канадэ' and hero.rare == 4 and hero.type == 'Охотник':
                    try: await bot.send_message(player1.user_id, "Нарушители порядка будут наказаны...")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Нарушители порядка будут наказаны...")
                    except: pass
                elif hero.name == 'Сейбер' and hero.rare == 4 and hero.type == 'Охотник':
                    try: await bot.send_message(player1.user_id, "Святой Грааль будет моим!")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Святой Грааль будет моим!")
                    except: pass
                elif hero.name == 'Даркнесс' and hero.rare == 4 and hero.type == 'Защитник':
                    try: await bot.send_message(player1.user_id, "Ааах... Я защищу всех от этого грязного извращенца, становитесь за мной, друзья!")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Ааах... Я защищу всех от этого грязного извращенца, становитесь за мной, друзья!")
                    except: pass
                elif hero.name == 'Мегумин' and hero.rare == 5 and hero.type == 'Особый':
                    try: await bot.send_message(player1.user_id, "Имя мне Мегумин!")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Имя мне Мегумин!")
                    except: pass
                elif hero.name == 'Ято' and hero.rare == 5 and hero.type == 'Охотник':
                    try: await bot.send_message(player1.user_id, "Лишь люди отделяют добро и зло, не боги. Проще говоря: «Богам всё дозволено». Они могут причинить боль и даже отнять жизнь. Это — Божья кара.")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Лишь люди отделяют добро и зло, не боги. Проще говоря: «Богам всё дозволено». Они могут причинить боль и даже отнять жизнь. Это — Божья кара.")
                    except: pass
                try: await bot.send_message(player2.user_id, text)
                except: pass
                await specialMoves(player1, player2, match, hero)
        elif user.id == player2.id:
            if hero.id not in [match.p2hero1, match.p2hero2, match.p2hero3, match.p2hero4, match.p2hero5]:
                if match.p2Mana < hero.rare:
                    try: await bot.send_message(call.message.chat.id, "У тебя не хватает энергии для призыва этой карты")
                    except: pass
                    return
                if not match.p2hero1: match.p2hero1 = hero.id
                elif not match.p2hero2: match.p2hero2 = hero.id
                elif not match.p2hero3: match.p2hero3 = hero.id
                elif not match.p2hero4: match.p2hero4 = hero.id
                elif not match.p2hero5: match.p2hero5 = hero.id
                else:
                    checkHero1 = await db.Inventory.get(id=match.p2hero1)
                    if checkHero1.nowhp <= 0:
                        match.p2hero1 = hero.id
                    else:
                        checkHero2 = await db.Inventory.get(id=match.p2hero2)
                        if checkHero2.nowhp <= 0:
                            match.p2hero2 = hero.id
                        else:
                            checkHero3 = await db.Inventory.get(id=match.p2hero3)
                            if checkHero3.nowhp <= 0:
                                match.p2hero3 = hero.id 
                            else:
                                checkHero4 = await db.Inventory.get(id=match.p2hero4)
                                if checkHero4.nowhp <= 0:
                                    match.p2hero4 = hero.id 
                                else:
                                    checkHero5 = await db.Inventory.get(id=match.p2hero5)
                                    if checkHero5.nowhp <= 0 :
                                        match.p2hero5 = hero.id
                                    else:
                                        text = "У тебя нет места для вызова карты. Максимальное количество карт на поле - 5!"
                                        try: await bot.send_message(call.message.chat.id, text)
                                        except: pass
                                        return
                if match.p2Mana >= hero.rare:
                    match.p2Mana -= hero.rare
                text = "Игроком {} на поле боя была призвана карта {} (/globalView_{})!".format(player2.username, hero.name, hero.idHero)
                await watcher(match, text)
                await logger.write(match, user.username, text)
                markup.add(InlineKeyboardButton('К полю', callback_data="match_view"))
                inMatch[user.id].append(hero.id)
                if hero.name == 'Аято' and hero.rare == 4 and hero.type == "Маг":
                    match.p2Mana += 1
                    match.p1Mana -= 1
                elif hero.name == 'Канадэ' and hero.rare == 4 and hero.type == 'Охотник':
                    killedName = None
                    checkCard = await db.Inventory.get_or_none(id=match.p1hero1)
                    if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                        checkCard.nowhp = 0
                        killedName = checkCard.name
                    else:
                        checkCard = await db.Inventory.get_or_none(id=match.p1hero2)
                        if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                            checkCard.nowhp = 0
                            killedName = checkCard.name
                        else:
                            checkCard = await db.Inventory.get_or_none(id=match.p1hero3)
                            if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                                checkCard.nowhp = 0
                                killedName = checkCard.name
                            else:
                                checkCard = await db.Inventory.get_or_none(id=match.p1hero4)
                                if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                                    checkCard.nowhp = 0
                                    killedName = checkCard.name
                                else:
                                    checkCard = await db.Inventory.get_or_none(id=match.p1hero5)
                                    if checkCard and checkCard.rare <= 3 and checkCard.nowhp > 0:
                                        checkCard.nowhp = 0
                                        killedName = checkCard.name
                    if killedName:
                        await checkCard.save()
                        try: await bot.send_message(player1.user_id, "Карта {} была уничтожена".format(killedName))
                        except: pass
                        try: await bot.send_message(player2.user_id, "Карта {} была уничтожена".format(killedName))
                        except: pass
                        text = "[{}]: Карта {} была уничтожена".format(user.username, killedName)
                        await watcher(match, text)
                        await logger.write(match, user.username, text)




                await match.save()
                await bot.edit_message_text("Призыв завершен.", call.message.chat.id, call.message.message_id, reply_markup=markup)
                if hero.name == 'Аято' and hero.rare == 4 and hero.type == "Маг":
                    match.p1Mana += 1
                    match.p2Mana -= 1
                    try: await bot.send_message(player1.user_id, "Пришло время предать вас забвению!")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Пришло время предать вас забвению!")
                    except: pass
                elif hero.name == 'Канадэ' and hero.rare == 4 and hero.type == 'Охотник':
                    try: await bot.send_message(player1.user_id, "Нарушители порядка будут наказаны...")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Нарушители порядка будут наказаны...")
                    except: pass
                elif hero.name == 'Сейбер' and hero.rare == 4 and hero.type == 'Охотник':
                    try: await bot.send_message(player1.user_id, "Святой Грааль будет моим!")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Святой Грааль будет моим!")
                    except: pass
                elif hero.name == 'Даркнесс' and hero.rare == 4 and hero.type == 'Защитник':
                    try: await bot.send_message(player1.user_id, "Ааах... Я защищу всех от этого грязного извращенца, становитесь за мной, друзья!")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Ааах... Я защищу всех от этого грязного извращенца, становитесь за мной, друзья!")
                    except: pass
                elif hero.name == 'Мегумин' and hero.rare == 5 and hero.type == 'Особый':
                    try: await bot.send_message(player1.user_id, "Имя мне Мегумин!")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Имя мне Мегумин!")
                    except: pass
                elif hero.name == 'Ято' and hero.rare == 5 and hero.type == 'Охотник':
                    try: await bot.send_message(player1.user_id, "Лишь люди отделяют добро и зло, не боги. Проще говоря: «Богам всё дозволено». Они могут причинить боль и даже отнять жизнь. Это — Божья кара.")
                    except: pass
                    try: await bot.send_message(player2.user_id, "Лишь люди отделяют добро и зло, не боги. Проще говоря: «Богам всё дозволено». Они могут причинить боль и даже отнять жизнь. Это — Божья кара.")
                    except: pass
                try: await bot.send_message(player1.user_id, text)
                except: pass
                await specialMoves(player1, player2, match, hero)




async def specialMoves(player1, player2, match, hero):
    user = await db.Users.get_or_none(id=hero.idplayer).first()
    if hero.name == 'Мегумин' and hero.rare == 5:
        if match.p1hero1:
            checkHero = await db.Inventory.get_or_none(id=match.p1hero1).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p1hero1).update(nowhp=F('nowhp') - 5)
                else:
                    # daily
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p1hero1).update(nowhp=0)
        if match.p2hero1:
            checkHero = await db.Inventory.get_or_none(id=match.p2hero1).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p2hero1).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p2hero1).update(nowhp=0)
        if match.p1hero2:
            checkHero = await db.Inventory.get_or_none(id=match.p1hero2).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p1hero2).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p1hero2).update(nowhp=0)
        if match.p2hero2:
            checkHero = await db.Inventory.get_or_none(id=match.p2hero2).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p2hero2).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p2hero2).update(nowhp=0)
        if match.p1hero3:
            checkHero = await db.Inventory.get_or_none(id=match.p1hero3).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p1hero3).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p1hero3).update(nowhp=0)
        if match.p2hero3:
            checkHero = await db.Inventory.get_or_none(id=match.p2hero3).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p2hero3).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p2hero3).update(nowhp=0)
        if match.p1hero4:
            checkHero = await db.Inventory.get_or_none(id=match.p1hero4).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p1hero4).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p1hero4).update(nowhp=0)
        if match.p2hero4:
            checkHero = await db.Inventory.get_or_none(id=match.p2hero4).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p2hero4).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p2hero4).update(nowhp=0)
        if match.p1hero5:
            checkHero = await db.Inventory.get_or_none(id=match.p1hero5).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p1hero5).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p1hero5).update(nowhp=0)
        if match.p2hero5:
            checkHero = await db.Inventory.get_or_none(id=match.p2hero5).first()
            if checkHero:
                if checkHero.nowhp - 5 > 0:
                    await db.Inventory.filter(id=match.p2hero5).update(nowhp=F('nowhp') - 5)
                else:
                    await db.Users.filter(id=user.id).update(killO=F('killO') + 1)
                    await db.Inventory.filter(id=match.p2hero5).update(nowhp=0)


async def calculate_win(match, player1, player2, winner):
    await match.refresh_from_db()
    if match.status == 5: return
    await db.Matches.filter(id=match.id).update(winner=winner.id, status=5)
    if match.tournament == 'unranked_standart': return await calculate_win_unranked_standart(match, player1, player2, winner)
    elif match.tournament == 'unranked_short': return calculate_win_unranked_short(match, player1, player2, winner)
    elif match.tournament == 'unranked_war': return calculate_win_unranked_war(match, player1, player2, winner)
    if winner.id == player1.id:
        if player1.elo - player2.elo < -800:
            winPts = 40
        elif player1.elo - player2.elo < -750:
            winPts = 39
        elif player1.elo - player2.elo < -700:
            winPts = 38
        elif player1.elo - player2.elo < -650:
            winPts = 37
        elif player1.elo - player2.elo < -600:
            winPts = 36
        elif player1.elo - player2.elo < -550:
            winPts = 35
        elif player1.elo - player2.elo < -500:
            winPts = 34
        elif player1.elo - player2.elo < -450:
            winPts = 33
        elif player1.elo - player2.elo < -400:
            winPts = 32
        elif player1.elo - player2.elo < -350:
            winPts = 31
        elif player1.elo - player2.elo < -300:
            winPts = 30
        elif player1.elo - player2.elo < -250:
            winPts = 29
        elif player1.elo - player2.elo < -200:
            winPts = 28
        elif player1.elo - player2.elo < -150:
            winPts = 27
        elif player1.elo - player2.elo < -100:
            winPts = 26
        elif player1.elo - player2.elo < 100:
            winPts = 25
        elif player1.elo - player2.elo < 150:
            winPts = 24
        elif player1.elo - player2.elo < 200:
            winPts = 23
        elif player1.elo - player2.elo < 250:
            winPts = 22
        elif player1.elo - player2.elo < 300:
            winPts = 21
        elif player1.elo - player2.elo < 350:
            winPts = 20
        elif player1.elo - player2.elo < 400:
            winPts = 19
        elif player1.elo - player2.elo < 450:
            winPts = 18
        elif player1.elo - player2.elo < 500:
            winPts = 17
        elif player1.elo - player2.elo < 550:
            winPts = 16
        elif player1.elo - player2.elo < 600:
            winPts = 15
        elif player1.elo - player2.elo < 650:
            winPts = 14
        elif player1.elo - player2.elo < 700:
            winPts = 13
        elif player1.elo - player2.elo < 750:
            winPts = 12
        elif player1.elo - player2.elo < 800:
            winPts = 11
        elif player1.elo - player2.elo > 850:
            winPts = 10
        else:
            winPts = 5

    elif winner.id == player2.id:
        if player2.elo - player1.elo < -800:
            winPts = 40
        elif player2.elo - player1.elo < -750:
            winPts = 39
        elif player2.elo - player1.elo < -700:
            winPts = 38
        elif player2.elo - player1.elo < -650:
            winPts = 37
        elif player2.elo - player1.elo < -600:
            winPts = 36
        elif player2.elo - player1.elo < -550:
            winPts = 35
        elif player2.elo - player1.elo < -500:
            winPts = 34
        elif player2.elo - player1.elo < -450:
            winPts = 33
        elif player2.elo - player1.elo < -400:
            winPts = 32
        elif player2.elo - player1.elo < -350:
            winPts = 31
        elif player2.elo - player1.elo < -300:
            winPts = 30
        elif player2.elo - player1.elo < -250:
            winPts = 29
        elif player2.elo - player1.elo < -200:
            winPts = 28
        elif player2.elo - player1.elo < -150:
            winPts = 27
        elif player2.elo - player1.elo < -100:
            winPts = 26
        elif player2.elo - player1.elo < 100:
            winPts = 25
        elif player2.elo - player1.elo < 150:
            winPts = 24
        elif player2.elo - player1.elo < 200:
            winPts = 23
        elif player2.elo - player1.elo < 250:
            winPts = 22
        elif player2.elo - player1.elo < 300:
            winPts = 21
        elif player2.elo - player1.elo < 350:
            winPts = 20
        elif player2.elo - player1.elo < 400:
            winPts = 19
        elif player2.elo - player1.elo < 450:
            winPts = 18
        elif player2.elo - player1.elo < 500:
            winPts = 17
        elif player2.elo - player1.elo < 550:
            winPts = 16
        elif player2.elo - player1.elo < 600:
            winPts = 15
        elif player2.elo - player1.elo < 650:
            winPts = 14
        elif player2.elo - player1.elo < 700:
            winPts = 13
        elif player2.elo - player1.elo < 750:
            winPts = 12
        elif player2.elo - player1.elo < 800:
            winPts = 11
        elif player2.elo - player1.elo > 850:
            winPts = 10
        else:
            winPts = 5
    print("win {}".format(winner.id))
    print("p1 elo {}".format(player1.elo))
    print("p2 elo {}".format(player2.elo))
    print("winPts {}".format(winPts))
    
    if winner.ladder:
        ladder = await db.Ladders.get_or_none(id=winner.ladder).first()
        if ladder and ladder.active == 2: await db.Users.filter(id=winner.id).update(ladderPts=F('ladderPts') + 1)

    if winner.id == player1.id:
        await db.Users.filter(id=player1.id).update(elo=F('elo') + winPts, hp=50, pvpPlayed=F('pvpPlayed') + 1, pvpWins=F('pvpWins') + 1, winsD=F('winsD') + 1, playD=F('playD') + 1)
        await db.Users.filter(id=player2.id).update(elo=F('elo') - winPts, hp=50, pvpPlayed=F('pvpPlayed') + 1, pvpLose=F('pvpLose') + 1, playD=F('playD') + 1)

    elif winner.id == player2.id:
        await db.Users.filter(id=player2.id).update(elo=F('elo') + winPts, hp=50, pvpPlayed=F('pvpPlayed') + 1, pvpWins=F('pvpWins') + 1, winsD=F('winsD') + 1, playD=F('playD') + 1)
        await db.Users.filter(id=player1.id).update(elo=F('elo') - winPts, hp=50, pvpPlayed=F('pvpPlayed') + 1, pvpLose=F('pvpLose') + 1, playD=F('playD') + 1)

    await db.Inventory.filter(idplayer=player1.id).update(nowhp=F('hp'))
    await db.Inventory.filter(idplayer=player2.id).update(nowhp=F('hp'))
