import random


def draw_pinus_fight(pinus_one_size, pinus_two_size, name1, name2):
    return f"Пинус игрока @{name1} \n 8{'=' * pinus_one_size}э \n Пинус игрока @{name2}\n 8{'=' * pinus_two_size}э"


def draw_pinus_personal(size_mod):
    return f"8{'=' * size_mod}э"


def personal_pinus(msg, bot):
    user_id = str(msg.from_user.id)
    size_mods = [round(int(digit) / 4 + random.randint(0, 9)) for digit in user_id]
    size_mod = sum(size_mods)
    bot.send_message(msg.chat.id,
                     f"{draw_pinus_personal(size_mod)} \n Твой пинус, @{msg.from_user.username}: {size_mod} см")
    bot.delete_message(msg.chat.id, msg.message_id)


def pinus_fight(msg, bot):
    user1_id = str(msg.from_user.id)
    user2_id = str(msg.reply_to_message.from_user.id)
    user1_name = msg.from_user.username
    user2_name = msg.reply_to_message.from_user.username

    sizes1 = [round(int(digit) / 4 + random.randint(0, 9)) for digit in user1_id]
    sizes2 = [round(int(digit) / 4 + random.randint(0, 9)) for digit in user2_id]
    pinus_one_size = sum(sizes1)
    pinus_two_size = sum(sizes2)

    if pinus_one_size > pinus_two_size:
        pinus_text = f"Пинус: @{user1_name} больше @{user2_name}"
    elif pinus_two_size > pinus_one_size:
        pinus_text = f"Пинус: @{user2_name} больше @{user1_name}"
    else:
        pinus_text = "Ваши пинусы равны"

    bot.send_message(msg.chat.id,
                     f'{draw_pinus_fight(pinus_one_size, pinus_two_size, user1_name, user2_name)} \n {pinus_text}')
    bot.delete_message(msg.chat.id, msg.message_id)