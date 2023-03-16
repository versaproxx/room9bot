def idi_v_pizdu(msg, bot):
    msg_id = msg.message_id
    if '@' in msg.text and '@pidor9bot' not in msg.text:
        name = msg.text.split('@')[1]
        bot.send_message(msg.chat.id, f'Иди в пизду, @{name}')
    else:
        try:
            name = msg.reply_to_message.from_user.username
            bot.send_message(msg.chat.id, f'Иди в пизду, @{name}', reply_to_message_id=msg.reply_to_message.message_id)
        except Exception as e:
            print(e)
            bot.send_message(msg.chat.id, 'Ой идите вы все в пизду, дамы и господа!')

    bot.delete_message(msg.chat.id, msg_id)
