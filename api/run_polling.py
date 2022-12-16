import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

from telegram import Bot
from telegram.ext import Updater

from api.settings import TELEGRAM_TOKEN
from bot.dispatcher import setup_dispatcher

def run_polling(tg_token: str = TELEGRAM_TOKEN):
    updater = Updater(tg_token, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(tg_token).get_me()
    # print(bot_info)
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    run_polling()