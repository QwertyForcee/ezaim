import telegram
from telegram import ChatAction, Update
from telegram.ext import CallbackContext

from bot.main import bot
from ezaim.models import User, TelegramUser, Loan


HELP_TEXT = """
This bot is designed to work with ezaim site.
After connection you can view your loans
To connect account use command /connect email
example: /connect user@gmail.com
To disconnect use command /disconnect
To view your loans use command /loans
"""

START_TEXT = """
Hello, it's ezaim bot. If you need help use /help command
"""

def start(update: Update, context: CallbackContext):
    update.message.reply_text(START_TEXT)


def help(update: Update, context: CallbackContext):
    update.message.reply_text(HELP_TEXT)

def connect(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if len(context.args) == 0:
        update.message.reply_text('You need to provide email in command message')
        return
    email = context.args[0]

    user = User.objects.filter(email=email)[:1]
    if len(user) == 0:
        update.message.reply_text(f"There are no accounts with email {email}")
        return
    user = user[0]
    res = list(TelegramUser.objects.filter(chat_id=chat_id))
    if len(res) == 1:
        update.message.reply_text(f"You're already connected to {user.email}")
        return

    if len(res) == 0:
        tg_user = TelegramUser(chat_id=chat_id, user=user, name=update.effective_user.name)
        tg_user.save()
        update.message.reply_text(f"Sent confirmation request to {email}. Confirm connection through site")
        return
    update.message.reply_text('Error: multiple connected accounts')
    

def disconnect(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    res = list(TelegramUser.objects.filter(chat_id=chat_id))

    if len(res) == 0:
        update.message.reply_text(f"You're not connected to any accounts")
        return
    tg_user = res[0]
    if len(res) == 1:
        email = tg_user.user.email
        tg_user.delete()
        update.message.reply_text(f"You're now disconnected from {email}")
        return
    update.message.reply_text('Error: multiple connected accounts')
        
def loans(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    res = list(TelegramUser.objects.filter(chat_id=chat_id))

    if len(res) == 0:
        update.message.reply_text('You need connected account to view loans')
        return
    if len(res) == 1:
        tg_user = res[0]
        if not tg_user.confirmed:
            update.message.reply_text('You need to confirm account from website to view loans')
            return
        loans = list(Loan.objects.filter(user=tg_user.user))
        if len(loans) == 0:
            update.message.reply_text("You don't have any loans")
            return
        reply = 'Your loans:'
        for loan in loans:
            reply += f'\n{loan}'
        update.message.reply_text(reply)
        return
    update.message.reply_text('Error: multiple connected accounts')
