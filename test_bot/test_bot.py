# -*- coding: utf-8 -*-
import telebot
import os
import validators
from selenium import webdriver
from pkg2 import config


# we make bot
TOKEN = config.token
bot = telebot.TeleBot(TOKEN, threaded=False)

# we configurate browser for correct work in headless mode

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

#we implement obligatory commands /start and /help

@bot.message_handler(commands=['start'])
def hello_user(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.username + "!")

@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(message.chat.id, 'To get screenshot of webpage use command /getpng.\nExample: /getpng https://www.google.com')


#we get a website screen using selenium and headless chrome
@bot.message_handler(commands=['getpng'])
def get_screenshot(message):
    uid = message.chat.id
    url = ""
    try:
        url = message.text.split(' ')[1]
    except IndexError:
        bot.send_message(uid, 'You have not entered URL!')
        return
    if not validators.url(url):
        bot.send_message(uid, 'URL is invalid!')
    else:
        photo_path = str(uid) + '.png'
        driver = webdriver.Chrome(chrome_options = options)
        driver.set_window_size(1280, 720)
        driver.get(url)
        driver.save_screenshot(photo_path)
        bot.send_photo(uid, photo = open(photo_path, 'rb'))
        driver.quit()
        os.remove(photo_path)


# run bot

if __name__ == '__main__':
    bot.infinity_polling()