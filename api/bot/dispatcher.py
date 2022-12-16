from telegram.ext import (
    Dispatcher, CommandHandler
)

from bot.main import bot
from api.settings import DEBUG
from bot.handlers import (
    start, help,
    connect, disconnect, loans
)

def setup_dispatcher(dp: Dispatcher):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('connect', connect))
    dp.add_handler(CommandHandler('disconnect', disconnect))
    dp.add_handler(CommandHandler('loans', loans))
    return dp

n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers))
