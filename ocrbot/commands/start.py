from ocrbot.helpers.decorators import send_typing_action
from telegram import Update
from telegram.ext import CallbackContext

@send_typing_action
def start(update:Update,context:CallbackContext):
    """Send a message when the command /start is issued."""
    first=update.effective_user.first_name
    update.message.reply_text('Hi! '+str(first)+' \n\nI am an Optical Character Recognizer Bot. \n\nJust send a clear image to me and i will recognize the text in the image and send it as a message!',quote=True)
