import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    if os.environ.get('ENV') == 'TEST':
        load_dotenv(dotenv_path=os.path.join(dirname, '..', '.env.test'))
    else:
        load_dotenv(dotenv_path=os.path.join(dirname, '..', '.env'))
except FileNotFoundError:
    pass

BOT_TOKEN = os.getenv('BOT_TOKEN')
SECRET = os.getenv('SECRET')
DATABASE_URL = os.getenv('DATABASE_URL')

# conversation handler states
UNAUTHORIZED, NAME, PLAYER, AVERAGE = 0, 1, 2, 3
