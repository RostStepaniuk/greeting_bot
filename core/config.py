import os
from dotenv import load_dotenv

load_dotenv()

user1 = os.environ.get('USER1')
user2 = os.environ.get('USER2')
id1 = os.environ.get('id1')
id2 = os.environ.get('id2')

TOKEN = os.environ.get('TOKEN')
GREETING = os.environ.get('GREETING')
GROUP_LINK = os.environ.get('GROUP_LINK')
WELCOME_TEXT = os.environ.get('GREETING')
ALLOWED_USERS = [ user1, user2]
ALLOWED_USER_IDS = {user1: id1, user2: id2} 
DB_URL = os.environ.get('DB_URL')

