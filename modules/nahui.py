def idi_na_huy(msg, bot):
    deleting_message = msg.message_id
    if '@' in str(msg.text):
        name = str(msg.text).split('@')[1]
        bot.reply_to(msg.reply_to_message.from_user.id, f'Иди на хуй, @{name}')
    else:
        try:
            name = msg.reply_to_message.from_user.username
            bot.send_message(msg.chat.id, f'Иди на хуй, @{name}',  reply_to_message_id=msg.reply_to_message.message_id)
        except Exception as e: 
            print('internal exc')
            print(e)
            bot.send_message(msg.chat.id, f'Да пошли вы все нахуй') 
        

    bot.delete_message(msg.chat.id, deleting_message)