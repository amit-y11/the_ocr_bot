from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from telegram import Update, Bot, ParseMode
import os
import json

#using cloudmersive api
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update,context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! \n\nWelcome to Optical Character Recognizer Bot. \n\nJust send a clear image to me and i will recognize the text in the image and send it as a message!\nTo get my contact details tap /contact')

def contact(update,context):
    """Send a message when the command /contact is issued."""
    update.message.reply_text("Hey! You can find me on \n[Telegram](https://telegram.me/amit_y11)", parse_mode=ParseMode.MARKDOWN)

def convert_image(update,context):
    filename="test.jpg"
    file_id = update.message.photo[-1].file_id
    newFile=context.bot.get_file(file_id)
    newFile.download(filename)
    update.message.reply_text("Yeah!,I got your image let me process it")
    
    configuration = cloudmersive_ocr_api_client.Configuration()
    API_KEY=os.environ.get("CLOUDMERSIVE_API","")
    configuration.api_key['Apikey'] = 'API_KEY'
    api_instance = cloudmersive_ocr_api_client.ImageOcrApi(cloudmersive_ocr_api_client.ApiClient(configuration))
    try:
        # Convert a photo of a document into text
        api_response = api_instance.image_ocr_post(filename)
        confidence=api_response.mean_confidence_level
        print(api_response)
        update.message.reply_text("Confidence level "+str(confidence)+" \nExtracted text:"+api_response.text_result)
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
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error) 
	
if __name__=="__main__":
	main()
