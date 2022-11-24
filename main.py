import telebot
import json
import urllib.request
import os
from dotenv import load_dotenv
import requests
load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode="HTML")
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
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['joke'])
def send_joke(message):
    bot.reply_to(message, '<b>Joke:</b> ' + joke + '\n<b>Punchline:</b> ' + punchline)


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
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Invalid Command')


bot.infinity_polling()
