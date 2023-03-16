def idi_na_huy(msg, bot):
    msg_id = msg.message_id
    if '@' in msg.text and '@pidor9bot' not in msg.text:
        name = msg.text.split('@')[1]
        bot.send_message(msg.chat.id, f'Иди на хуй, @{name}')
    else:
        try:
            name = msg.reply_to_message.from_user.username
            bot.send_message(msg.chat.id, f'Иди на хуй, @{name}', reply_to_message_id=msg.reply_to_message.message_id)
        except Exception as e:
            bot.send_message(msg.chat.id, 'Да пошли вы все нахуй')

    bot.delete_message(msg.chat.id, msg_id)
