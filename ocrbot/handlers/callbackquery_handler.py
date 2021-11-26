import requests
from ocrbot.helpers.decorators import send_typing_action
from telegram import Update
from telegram.ext import CallbackContext
from ocrbot.helpers.mock_database import get_file_path
from ocrbot.config import API_KEY



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
