from telegram import ChatAction,InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler,PicklePersistence, CallbackContext
import logging
import os
from functools import wraps
import requests
from config import API_KEY, BOT_TOKEN

from mock_database import get_file_path, insert_file_path


# decorator for sending typing chat action
def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and context
#Your bot will repond when you type / and then respective commands e.g /start , /help
@send_typing_action
def start(update:Update,context:CallbackContext):
    """Send a message when the command /start is issued."""
    first=update.effective_user.first_name
    update.message.reply_text('Hi! '+str(first)+' \n\nI am an Optical Character Recognizer Bot. \n\nJust send a clear image to me and i will recognize the text in the image and send it as a message!',quote=True)


@send_typing_action
def convert_image(update:Update,context:CallbackContext):
    '''
    This function is called when the user sends a photo.
    '''
    chat_id=update.effective_chat.id
    file_id = update.message.photo[-1].file_id
    newFile=context.bot.get_file(file_id)
    file_path= newFile.file_path

    keyboard = [[InlineKeyboardButton("English ", callback_data='eng'), InlineKeyboardButton("Russian", callback_data='rus'),InlineKeyboardButton("Czech", callback_data='cze')],
                [InlineKeyboardButton("Chinese simplified", callback_data='chs'), InlineKeyboardButton("Chinese Traditional", callback_data='cht')],[InlineKeyboardButton("Japanese", callback_data='jpn')] ,
                [InlineKeyboardButton("Arabic", callback_data='ara'),InlineKeyboardButton("Afrikans", callback_data='AFR'), InlineKeyboardButton("German", callback_data='gre')],
                [InlineKeyboardButton("Italian", callback_data='ita'),InlineKeyboardButton("Indonesian", callback_data='eng'),InlineKeyboardButton("French", callback_data='fre')],
                [InlineKeyboardButton ("Spanish", callback_data='spa'),InlineKeyboardButton("Portuguese", callback_data='por'),InlineKeyboardButton("Korean", callback_data='kor')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    m = update.message.reply_text('Select Language : ', reply_markup=reply_markup,quote=True)
    insert_file_path(chat_id,m.message_id,file_path)

@send_typing_action
def button_click(update:Update,context:CallbackContext):
    '''
    This function is called when the user clicks on the buttons.
    '''
    query = update.callback_query
    query.answer()
    filepath=get_file_path(query.message.chat_id,query.message.message_id)
    if filepath is not None:
        query.edit_message_text("Extracting text please wait ...")
        data=requests.get(f"https://api.ocr.space/parse/imageurl?apikey={API_KEY}&url={filepath}&language={query.data}&detectOrientation=True&filetype=JPG&OCREngine=1&isTable=True&scale=True")
        data=data.json()
        if data['IsErroredOnProcessing']==False:
            message=data['ParsedResults'][0]['ParsedText']
            query.edit_message_text(f"{message}")
        else:
            query.edit_message_text(text="⚠️Something went wrong, please try again later ⚠️")
    else:
        query.edit_message_text("Something went wrong, Send this image again")


def invalid_command(update:Update, context:CallbackContext):
    """
    This function is called when the user enters an invalid command.
    """
    update.message.reply_text("Invalid command. Type /help for a list of commands.")


def help(update:Update,context:CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "List of commands available:\
        \n/start - To start the bot\
        \n/help - To show this message",quote=True
    )

def main(): 
    updater = Updater(BOT_TOKEN,use_context=True)
    updater.bot.set_my_commands([("start","start the bot"),("help","Get list of commands")])
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start,run_async=True))
    dp.add_handler(CommandHandler('help',help,run_async=True))
    dp.add_handler(MessageHandler(Filters.photo, convert_image,run_async=True))
    dp.add_handler(MessageHandler(Filters.regex("^\/.*$"),invalid_command,run_async=True))
    dp.add_handler(CallbackQueryHandler(button_click,run_async=True))

    updater.start_polling(drop_pending_updates=True)
    print("Bot is running")
    updater.idle()
 
	
if __name__=="__main__":
	main()
