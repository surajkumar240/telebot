import json
import os
import urllib.request
import requests
from dotenv import load_dotenv
from telebot import *

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

print("Bot Started..........")

# joke start
jokeurl = "https://official-joke-api.appspot.com/random_joke"
jokedata = urllib.request.urlopen(jokeurl).read().decode()
# parse json object
jokeobj = json.loads(jokedata)
joke = jokeobj['setup']
punchline = jokeobj['punchline']
# joke end

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = str(message.chat.first_name)
    bot.send_message(message.chat.id, f"Hello {user_first_name}, use the menu to give commands to the bot")


@bot.message_handler(commands=['stop'])
def send_welcome(message):
    user_first_name = str(message.chat.first_name)
    bot.send_message(message.chat.id, text=f"Bye {user_first_name}!")


@bot.message_handler(commands=['joke'])
def send_joke(message):
    bot.reply_to(message, '<b>Joke:</b> ' + joke + '\n<b>Punchline:</b> ' + punchline, parse_mode="HTML")


@bot.message_handler(commands=['joke'])
def send_joke(message):
    bot.reply_to(message, '<b>Joke:</b> ' + joke + '\n<b>Punchline:</b> ' + punchline)


def get_url():
    contents = requests.get('https://meme-api.herokuapp.com/gimme').json()
    image_url = contents['url']
    return image_url


@bot.message_handler(commands=['meme'])
def msg4(message):
    url = get_url()
    bot.send_photo(message.chat.id, url)


@bot.message_handler(commands=['about'])
def numbermsg(message):
    msg = bot.reply_to(message, 'Enter Number')
    bot.register_next_step_handler(msg, number_step)


def number_step(message):
    num = message.text
    answer = requests.get(f'http://numbersapi.com/{num}?json')
    bot.send_message(message.chat.id, json.loads(answer.text)['text'])


@bot.message_handler(commands=['urlshorten'])
def urlmsg(message):
    longurl = bot.reply_to(message, 'Enter url')
    bot.register_next_step_handler(longurl, url_step)


def url_step(message):
    lurl = message.text
    answer = requests.get(f'https://api.shrtco.de/v2/shorten?url={lurl}')
    surl = json.loads(answer.text)['result']['short_link']
    bot.send_message(message.chat.id, f"Short URL: {surl}")


@bot.message_handler(commands=['qrgen'])
def qrmsg(message):
    qrurl = bot.reply_to(message, 'Enter URL')
    bot.register_next_step_handler(qrurl, qrimage)


def qrimage(message):
    qrlink = message.text
    image_url = f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qrlink}'
    bot.send_photo(message.chat.id, image_url)
    bot.send_message(message.chat.id, f"QR generated successfully for {qrlink}")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Invalid Command')


bot.infinity_polling()
