# -*- coding: utf-8 -*-

import telebot
import os
from flask import Flask, request
import config
import lyrics as ly
import random
from telebot import types
import logging

bot = telebot.TeleBot(config.token)

def cunnilingus():
    cuni = ['Great taste!\n', 'Great music!\n', 'You have an excellent taste!\n',
            'Your preferences are great!\n', 'Fapping for your music!\n',
            'Masturbate for your music!\n', 'Enjoy!\n', 'I like your music bro!\n',
            'I could not restrain myself and also listened to!\n']
    return random.choice(cuni)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    # bot.send_message(message.chat.id, message.text)
    greeting = "Hi! Send me 'Artist - Song"
    bot.send_message(message.chat.id, greeting)


@bot.message_handler(content_types=["text"])
def get_lyrics(message):
    bot.send_message(message.chat.id, "Looking for lyrics, wait...")
    link, sp_link = ly.by_title(message.text)

    markup = types.InlineKeyboardMarkup()
    if sp_link:
        btn_my_site = types.InlineKeyboardButton(text='Spotify', url=str(sp_link))
        markup.add(btn_my_site)
    bot.send_message(message.chat.id, cunnilingus() + link, reply_markup=markup)


# @server.route("/bot", methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200
#
#
# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url="https://liricsreally.herokuapp.com/")
#     return "!", 200
#
#
# server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8443)))


# Здесь пишем наши хэндлеры

# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://liricsreally.herokuapp.com/") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT', 80)))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
