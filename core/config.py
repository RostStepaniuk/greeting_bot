import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')
GREETING = os.environ.get('GREETING')
GROUP_LINK = os.environ.get('GROUP_LINK')
WELCOME_TEXT = os.environ.get('GREETING')
ALLOWED_USERS = ['nemchena', 'slimshady_rost']
ALLOWED_USER_IDS = {'slimshady_rost':1861763218, 'nemchena':914118651} 
