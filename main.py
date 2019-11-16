import os
from flask import Flask, request
import telebot


INFO = "{0}\nId: {1}\nFirst: {2}\nLast: {3}\nLang: {4}"
GREETING = "Hi, {0}!"
TOKEN = os.getenv('TG_API_TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message, GREETING.format(message.from_user.first_name))
    # bot.reply_to(message, 'Привет, %s!' % message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, INFO.format(
        message.from_user.username,
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.language_code,
    ))


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '', 200


if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv('WEBHOOK_URL') + TOKEN)
    server.run(host="0.0.0.0", port=int(os.getenv('PORT', 8443)))
