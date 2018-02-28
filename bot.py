# -*- coding: utf-8 -*-

# import telebot
# import os
# from flask import Flask, request
# import config
# import lyrics as ly
# import random
# from telebot import types
#
# bot = telebot.TeleBot(config.token)
# server = Flask(__name__)
#
#
# def cunnilingus():
#     cuni = ['Great taste!\n', 'Great music!\n', 'You have an excellent taste!\n',
#             'Your preferences are great!\n', 'Fapping for your music!\n',
#             'Masturbate for your music!\n', 'Enjoy!\n', 'I like your music bro!\n',
#             'I could not restrain myself and also listened to!\n']
#     return random.choice(cuni)
#
#
# @bot.message_handler(commands=['start', 'help'])
# def handle_start_help(message):
#     # bot.send_message(message.chat.id, message.text)
#     greeting = "Hi! Send me 'Artist - Song"
#     bot.send_message(message.chat.id, greeting)
#
#
# @bot.message_handler(content_types=["text"])
# def get_lyrics(message):
#     bot.send_message(message.chat.id, "Looking for lyrics, wait...")
#     link, sp_link = ly.by_title(message.text)
#
#     markup = types.InlineKeyboardMarkup()
#     if sp_link:
#         btn_my_site = types.InlineKeyboardButton(text='Spotify', url=str(sp_link))
#         markup.add(btn_my_site)
#     bot.send_message(message.chat.id, cunnilingus() + link, reply_markup=markup)
#
#
# @server.route("/", methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200
#
#
# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url="https://liricsreally.herokuapp.com/" + config.token)
#     return "!", 200
#
#
# if __name__ == "__main__":
#     server = Flask(__name__)
#     server.run(host="0.0.0.0", port=int(3334))
#     server = Flask(__name__)

import os
import config
import telebot
from flask import Flask, request

TOKEN = config.token
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://liricsreally.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
