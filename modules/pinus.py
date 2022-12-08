import random
def personal_pinus(msg, bot):
    raw_pinus = str(msg.from_user.id)
    for raw_size in raw_pinus:
        size = 0
        size += int(raw_size)
    size_mod = round((size / 4) + random.randint(0,9))
    pinus_grapg = f"8{'='*size_mod}-)"
    bot.send_message(msg.chat.id, f"{pinus_grapg}")
    bot.send_message(msg.chat.id, f"Твой пинус: {size_mod}")
    bot.delete_message(msg.chat.id, msg.message_id)

def pinus_fight(msg, bot):
    pinus_one = str(msg.from_user.id)
    pinus_two = str(msg.reply_to_message.from_user.id)
    pinus_one_size = 0
    pinus_two_size = 0
    size_mod_one = round((pinus_one_size / 4) + random.randint(0,9))
    size_mod_two = round((pinus_two_size / 4) + random.randint(0,9))

    for pinus in pinus_one:
        pinus_one_size += round(int(pinus) / 4 + random.randint(0,9))
    for pinus in pinus_two:
        pinus_two_size += round(int(pinus) / 4 + random.randint(0,9))
    if pinus_one_size > pinus_two_size:
        bot.send_message(msg.chat.id, f"Пинус игрока @{msg.from_user.username} \n 8{'='*pinus_one_size}-) \n Пинус игрока @{msg.reply_to_message.from_user.username}\n 8{'='*pinus_two_size}-)")
        bot.send_message(msg.chat.id, f"Пинус: @{msg.from_user.username} больше @{msg.reply_to_message.from_user.username}")
    if pinus_two_size > pinus_one_size:
        bot.send_message(msg.chat.id, f"Пинус игрока @{msg.from_user.username} \n 8{'='*pinus_one_size}-) \n Пинус игрока @{msg.reply_to_message.from_user.username}\n 8{'='*pinus_two_size}-)")
        bot.send_message(msg.chat.id, f"Пинус: @{msg.reply_to_message.from_user.username} больше @{msg.from_user.username}")    
    if pinus_one_size == pinus_two_size:
        bot.send_message(msg.chat.id, f"Пинус игрока @{msg.from_user.username} \n 8{'='*pinus_one_size}-) \n Пинус игрока @{msg.reply_to_message.from_user.username}\n 8{'='*pinus_two_size}-)")
        bot.send_message(msg.chat.id, f"Ваши пинусы равны")
    bot.delete_message(msg.chat.id, msg.message_id)