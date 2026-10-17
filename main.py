import telebot
from config import token
from logic import Pokemon


bot = telebot.TeleBot(token)


@bot.message_handler(commands=["go"])
def go(message):
    trainer = (
        message.from_user.username
        or str(message.from_user.id)
    )

    if trainer in Pokemon.pokemons:
        bot.reply_to(
            message,
            "Вы уже создали покемона."
        )
        return

    pokemon = Pokemon(trainer)

    bot.send_message(
        message.chat.id,
        pokemon.info()
    )

    if pokemon.show_img():
        bot.send_photo(
            message.chat.id,
            pokemon.show_img()
        )


bot.infinity_polling(none_stop=True)

