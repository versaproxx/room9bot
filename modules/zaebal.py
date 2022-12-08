def zaebal(msg, bot):
    deleting_message = msg.message_id
    if '@' in str(msg.text) and not '@pidor9bot' in str(msg.text):
        name = str(msg.text).split('@')[1]
        bot.send_message(msg.chat.id, f'Ты заебал, @{name}')
    else:
        try:
            name = msg.reply_to_message.from_user.username
            bot.send_message(msg.chat.id, f'Ты заебал, @{name}',  reply_to_message_id=msg.reply_to_message.message_id)
        except Exception as e: 
            print(e)
            bot.send_message(msg.chat.id, f'Как же вы все меня заебали') 
        

    bot.delete_message(msg.chat.id, deleting_message)