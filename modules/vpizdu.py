def idi_v_pizdu(msg, bot):
    deleting_message = msg.message_id
    if '@' in str(msg.text):
        name = str(msg.text).split('@')[1]
        try:
            bot.reply_to(msg.reply_to_message.from_user.id, f'Иди в пизду, @{name}')
        except Exception as e: 
            print('internal exc')
            print(e)
            bot.send_message(msg.chat.id, f'Ой идите вы все в пизду, дамы и господа!')
    else:
        try:
            name = msg.reply_to_message.from_user.username
            bot.send_message(msg.chat.id, f'Иди в пизду, @{name}',  reply_to_message_id=msg.reply_to_message.message_id)
        except Exception as e: 
            print(e)
            bot.send_message(msg.chat.id, f'Ой идите вы все в пизду, дамы и господа!') 
        

    bot.delete_message(msg.chat.id, deleting_message)