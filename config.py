import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.environ.get("API_KEY","") # api key from https://ocr.space/ocrapi
BOT_TOKEN = os.environ.get("BOT_TOKEN","") # bot token from @BotFather