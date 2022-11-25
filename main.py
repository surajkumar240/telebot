import json
import os
import urllib.request
import requests
from dotenv import load_dotenv
from telebot import *

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))
# joke start
jokeurl = "https://official-joke-api.appspot.com/random_joke"
jokedata = urllib.request.urlopen(jokeurl).read().decode()
# parse json object
jokeobj = json.loads(jokedata)
joke = jokeobj['setup']
punchline = jokeobj['punchline']
# joke end
commands = {  # command description used in the "help" command
    'start': 'Start the bot',
    'help': 'Gives you information about the available commands',
    'joke': 'Random jokes',
    'meme': 'Random memes',
    'urlshorten': 'Shorten URLs',
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = str(message.chat.first_name)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton("/joke")
    btn2 = types.KeyboardButton("/meme")
    btn3 = types.KeyboardButton("/urlshorten")
    btn4 = types.KeyboardButton("/qrgen")
    btn5 = types.KeyboardButton("/stop")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(chat_id=message.chat.id, text=f"Choose a command {user_first_name}", reply_markup=markup)


@bot.message_handler(commands=['stop'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=message.chat.id, text="Bye!", reply_markup=markup)


@bot.message_handler(commands=['joke'])
def send_joke(message):
    bot.reply_to(message, '<b>Joke:</b> ' + joke + '\n<b>Punchline:</b> ' + punchline, parse_mode="HTML")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


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
    qrurl = bot.reply_to(message, 'Enter url')
    bot.register_next_step_handler(qrurl, qrimage)


def qrimage(message):
    qrlink = message.text
    image_url = f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qrlink}'
    bot.send_photo(message.chat.id, image_url)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Invalid Command')


bot.infinity_polling()
