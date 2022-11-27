import json
import os
import urllib.request
import requests
from dotenv import load_dotenv
from telebot import *

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))
happikey = os.getenv("PASSAPI")
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
    contents = requests.get('https://api.thesurajkumar.tk/getmeme').json()
    image_url = contents['url']
    return image_url


@bot.message_handler(commands=['meme'])
def msg4(message):
    url = get_url()
    bot.send_photo(message.chat.id, url)


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
    image_url = f'https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={qrlink}&format=png'
    ct = f'Successfully generated QR for {qrlink}'
    bot.send_photo(message.chat.id, image_url, caption={ct})


@bot.message_handler(commands=['passwordgen'])
def passmsg(message):
    passlen = bot.reply_to(message, 'Enter max length')
    bot.register_next_step_handler(passlen, pass_gen)


def pass_gen(message):
    maxlen = message.text

    answer = requests.get(
        f'https://api.happi.dev/v1/generate-password?apikey={happikey}&limit=1&length={maxlen}&num=1&upper=1&symbols=1')
    finpass = json.loads(answer.text)['passwords']
    bot.send_message(message.chat.id, f"Password: `{finpass}`", parse_mode="Markdown")


@bot.message_handler(commands=['weather'])
def weathermsg(message):
    cityname = bot.reply_to(message, 'Enter city name')
    bot.register_next_step_handler(cityname, weather_gen)


def weather_gen(message):
    cityn = message.text
    wtoken = os.getenv("WTOKEN")
    answer = requests.get(
        f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{cityn}?unitGroup=metric&key={wtoken}&contentType=json')
    cityl = json.loads(answer.text)['resolvedAddress']
    maxtemp = json.loads(answer.text)['days'][0]['tempmax']
    mintemp = json.loads(answer.text)['days'][0]['tempmin']
    winds = json.loads(answer.text)['days'][0]['windspeed']
    humidity = json.loads(answer.text)['days'][0]['humidity']
    bot.send_message(message.chat.id,
                     f"<b>Region:</b> {cityl} \n<b>Maximum Temperature:</b> {maxtemp}°C \n<b>Minimum Temperature:</b> {mintemp}°C \n<b>Windspeed:</b> {winds} km/h \n<b>Humidity:</b> {humidity}%",
                     parse_mode="HTML")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Invalid Command')


bot.infinity_polling()
