import telegram.ext
import responses as r
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

print("Bot started....")


def start_command(update, context):
    update.message.reply_text('Type something')


def help_command(update, context):
    update.message.reply_text('Ask google')


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = r.sample_responses(text)

    update.message.reply_text(response)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(telegram.ext.CommandHandler("start", start_command))
    dp.add_handler(telegram.ext.CommandHandler("help", help_command))

    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()
