from telegram import Bot

from api.settings import TELEGRAM_TOKEN

bot = Bot(TELEGRAM_TOKEN)
TG_BOT_USERNAME = bot.get_me()['username']
