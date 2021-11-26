from telegram import Update
from telegram.ext import CallbackContext
from ocrbot.helpers.decorators import send_typing_action

@send_typing_action
def help(update:Update,context:CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "List of commands available:\
        \n/start - To start the bot\
        \n/help - To show this message",quote=True
    )