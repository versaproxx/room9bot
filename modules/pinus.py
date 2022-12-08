import random
def draw_pinus_fight(pinus_one_size, pinus_two_size, name1, name2):
    return f"Пинус игрока @{name1} \n 8{'='*pinus_one_size}э \n Пинус игрока @{name2}\n 8{'='*pinus_two_size}э"

def draw_pinus_personal(size_mod):
    return f"8{'='*size_mod}э"

def personal_pinus(msg, bot):
    raw_pinus = str(msg.from_user.id)
    for raw_size in raw_pinus:
        size = 0
        size += int(raw_size)
    size_mod = round((size / 4) + random.randint(0,9))
    bot.send_message(msg.chat.id, f"{draw_pinus_personal(size_mod)}")
    bot.send_message(msg.chat.id, f"Твой пинус: {size_mod}")
    bot.delete_message(msg.chat.id, msg.message_id)

def pinus_fight(msg, bot):
    pinus_one = str(msg.from_user.id)
    pinus_two = str(msg.reply_to_message.from_user.id)
    name1 = str(msg.from_user.username)
    name2 = str(msg.reply_to_message.from_user.username)
    pinus_one_size = 0
    pinus_two_size = 0
    for pinus in pinus_one:
        pinus_one_size += round(int(pinus) / 4 + random.randint(0,9))
    for pinus in pinus_two:
        pinus_two_size += round(int(pinus) / 4 + random.randint(0,9))
    
    bot.send_message(msg.chat.id, draw_pinus_fight(pinus_one_size, pinus_two_size, name1, name2))
    if pinus_one_size > pinus_two_size:
        bot.send_message(msg.chat.id, f"Пинус: @{msg.from_user.username} больше @{msg.reply_to_message.from_user.username}")
    if pinus_two_size > pinus_one_size:
        bot.send_message(msg.chat.id, f"Пинус: @{msg.reply_to_message.from_user.username} больше @{msg.from_user.username}")    
    if pinus_one_size == pinus_two_size:
        bot.send_message(msg.chat.id, f"Ваши пинусы равны")
    bot.delete_message(msg.chat.id, msg.message_id)