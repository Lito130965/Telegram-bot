from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
api_id = getenv('api_id')
api_hash = getenv('api_hash')
MONGO_uri = getenv('MONGO_uri')
