import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

bot.send_message("260945403", "test_bot")

#bot.polling(none_stop=True)