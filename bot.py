import telegram
from telegram import ChatAction,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
import logging
import os
import json
from functools import wraps

#using cloudmersive api
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException

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
@run_async     
@send_typing_action
def start(update,context):
    """Send a message when the command /start is issued."""
    global first
    first=update.message.chat.first_name
    update.message.reply_text('Hi! '+str(first)+' \n\nWelcome to Optical Character Recognizer Bot. \n\nJust send a clear image to me and i will recognize the text in the image and send it as a message!\nTo get my contact details tap /contact')

@run_async
@send_typing_action
def contact(update,context):
    """Send a message when the command /contact is issued."""
    update.message.reply_text("Hey! You can find me on \n[Telegram](https://telegram.me/amit_y11)", parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text("Join channel : @botsbyamit \nIf you have any questions ask on Group : @botsbyamit_support")

@run_async
@send_typing_action
def convert_image(update,context):
    global filename
    filename="testing.jpg"
    global file_id
    file_id = update.message.photo[-1].file_id
    newFile=context.bot.get_file(file_id)
    newFile.download(filename)
    #Till now we downloaded the image file
    global chat_id
    chat_id=update.message.chat_id
    context.bot.send_message(chat_id=chat_id , text="Yeah!,I got your image let me process it")
    
    # Now we are using inline keyboard for getting the language input from user
    keyboard = [[InlineKeyboardButton("English ", callback_data='ENG'),InlineKeyboardButton("Hindi", callback_data='HIN'), InlineKeyboardButton("Russian", callback_data='RUS'),InlineKeyboardButton("Czech", callback_data='CES')],
                [InlineKeyboardButton("Chinese simplified", callback_data='ZHO'), InlineKeyboardButton("Chinese Traditional", callback_data='ZHO-HANT'),InlineKeyboardButton("Japanese", callback_data='JPA'),InlineKeyboardButton("Indonesian", callback_data='IND')] ,
                [InlineKeyboardButton("Arabic", callback_data='ARA'),InlineKeyboardButton("Afrikans", callback_data='AFR'), InlineKeyboardButton("German", callback_data='DEU'),InlineKeyboardButton("French", callback_data='FRA')],
                [InlineKeyboardButton("Italian", callback_data='ITA'), InlineKeyboardButton("Urdu", callback_data='URD'),InlineKeyboardButton("Malayalam", callback_data='MAL'),InlineKeyboardButton("Tamil", callback_data='TAM')],
                [InlineKeyboardButton("Hebrew", callback_data='HEB'), InlineKeyboardButton ("Bengali" , callback_data='BEN'), InlineKeyboardButton ("Spanish", callback_data='SPA'), InlineKeyboardButton ("Persian",callback_data='FAS')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Select Language : ', reply_markup=reply_markup)
    return convert_image

@run_async
def button(update, context):
    global query
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Selected Language is: {}".format(query.data))
    

    configuration = cloudmersive_ocr_api_client.Configuration()
    #Enter Your cloudmersive api key in place of  os.environ.get(...........)
    configuration.api_key['Apikey'] = os.environ.get("CLOUDMERSIVE_API","")
    api_instance = cloudmersive_ocr_api_client.ImageOcrApi(cloudmersive_ocr_api_client.ApiClient(configuration))
    try:
        lang=query.data
        api_response = api_instance.image_ocr_post(filename,language=lang)
        confidence=api_response.mean_confidence_level
        context.bot.send_message(chat_id=chat_id , text="Confidence : "+str(confidence*100)+"% \nExtracted text:\n")
        context.bot.send_message(chat_id=chat_id , text=api_response.text_result)
    except ApiException as e:
        context.bot.send_message(chat_id=chat_id , text="Exception when calling ImageOcrApi->image_ocr_photo_to_text: %s\n" % e)
        try:
            os.remove('testing.jpg')
        except Exception:
            pass
    return button
    
def donate(update,context):
	update.message.reply_text("You can support me by donating any amount you wish to me using the following *Payment Options*: \n\n[Paypal](https://paypal.me/yamit11) \nUPI : `amity11@kotak` \n[Debit/Credit/Other wallets](https://rzp.io/l/amity11)\n\nDon't forget to send a screenshot of the transaction to @amit_y11",parse_mode=ParseMode.MARKDOWN)
    return donate
	
def main(): 
    bot_token=os.environ.get("BOT_TOKEN", "")
    updater = Updater(bot_token,use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('contact', contact))
    dp.add_handler(CommandHandler('donate', donate))
    dp.add_handler(MessageHandler(Filters.photo, convert_image))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()
 
	
if __name__=="__main__":
	main()
