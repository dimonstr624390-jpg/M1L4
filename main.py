import telebot
import random
from config import token

from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        number = random.randint(1, 3)
        if number == 1:
            pokemon = Wizard(message.from_user.username)
        elif number == 2:
            pokemon = Fighter(message.from_user.username)
        else:
            pokemon = Pokemon(message.from_user.username)
            
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


@bot.message_handler(commands=["attack"])
def attack(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons and message.from_user.username in Pokemon.pokemons:
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            result = pok.attack(enemy) 
            bot.reply_to(message, result if result else f"@{pok.username} атаковал @{enemy.username}!")
        else:
            bot.reply_to(message, "Убедитесь, что у обоих игроков созданы покемоны.")
    else:
        bot.reply_to(message, "Нужно отправить команду ответом на сообщение")



bot.infinity_polling(none_stop=True)
