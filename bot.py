import telegram
from telegram import ChatAction
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import json
from functools import wraps
from time import sleep
import time

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

#using cloudmersive api
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
@run_async
@send_typing_action
def start(update,context):
    """Send a message when the command /start is issued."""
    time.sleep(.500)
    update.message.reply_text('Hi! \n\nWelcome to Optical Character Recognizer Bot. \n\nJust send a clear image to me and i will recognize the text in the image and send it as a message!\nTo get my contact details tap /contact')

@run_async
@send_typing_action
def contact(update,context):
    """Send a message when the command /contact is issued."""
    time.sleep(.500)
    update.message.reply_text("Hey! You can find me on \n[Telegram](https://telegram.me/amit_y11)\nJoin channel : @botsbyamit \nIf you have any question ask on Group : @botsbyamit_support", parse_mode=telegram.ParseMode.MARKDOWN_V2)

@run_async
@send_typing_action
def convert_image(update,context):
    filename="testing.jpg"
    file_id = update.message.photo[-1].file_id
    newFile=context.bot.get_file(file_id)
    newFile.download(filename)
    time.sleep(1)
    update.message.reply_text("Yeah!,I got your image let me process it")
    
    configuration = cloudmersive_ocr_api_client.Configuration()
    
    configuration.api_key['Apikey'] = os.environ.get("CLOUDMERSIVE_API","")
    api_instance = cloudmersive_ocr_api_client.ImageOcrApi(cloudmersive_ocr_api_client.ApiClient(configuration))
    try:
        # Convert a photo of a document into text
        api_response = api_instance.image_ocr_post(filename)
        confidence=api_response.mean_confidence_level
        update.message.reply_text("Confidence : "+str(confidence*100)+"% \nExtracted text:\n")
        update.message.reply_text(api_response.text_result)
    except ApiException as e:
        update.message.reply_text("Exception when calling ImageOcrApi->image_ocr_photo_to_text: %s\n" % e)
        try:
            os.remove('testing.jpg')
        except Exception:
            pass
	
def main():
    ocr_bot_token=os.environ.get("BOT_TOKEN", "")
    updater = Updater(ocr_bot_token,use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('contact', contact))
    dp.add_handler(MessageHandler(Filters.photo, convert_image))
    updater.start_polling()
    updater.idle()
 
	
if __name__=="__main__":
	main()
