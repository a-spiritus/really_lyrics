# -*- coding: utf-8 -*-

import telebot
import config
import lyrics as ly
import random
from telebot import types

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


if __name__ == "__main__":
    bot.polling(none_stop=True)
