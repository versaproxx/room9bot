def idi_na_huy(msg, bot):
    deleting_message = msg.message_id
    if '@' in str(msg.text):
        name = str(msg.text).split('@')[1]
        bot.reply_to(msg.reply_to_message.from_user.id, f'Иди на хуй, @{name}')
    else:
        try:
            name = msg.reply_to_message.from_user.username
            bot.send_message(msg.chat.id, f'Иди на хуй, @{name}',  reply_to_message_id=msg.reply_to_message.message_id)
        except:
            bot.send_message(msg.chat.id, f'Ты, засранец вонючий, мать твою, а? Ну, иди сюда, попробуй меня трахнуть – я тебя сам трахну, ублюдок, онанист чертов, будь ты проклят! Иди, идиот, трахать тебя и всю твою семью! Говно собачье, жлоб вонючий, дерьмо, сука, падла! Иди сюда, мерзавец, негодяй, гад! Иди сюда, ты, говно, жопа!') 
        

    bot.delete_message(msg, deleting_message)