from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_uri
import dns.resolver
from bson.json_util import dumps

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
uri = MONGO_uri
client = MongoClient(uri)

telegram_db = client.telegramDB
members_collection = telegram_db.members

def insert_member_to_db(member):
    """ Inserting document to MongoDB """
    member = eval(member.replace('false', '0').replace('true', '1'))
    #
    members_collection.insert_one(member)

def set_emoji_to_user(user_id, emoji):
    """ Setting emoji to existing in MongoDB user """
    changes = {'$set': {'emoji': emoji}}
    members_collection.update_one({'id': user_id}, changes)
    return {'message': 'ok'}

def get_all_members_from_db() -> list:
    """ Return list of all members from MongoDB """
    return list(members_collection.find({}))

def get_all_members_id_from_db() -> list:
    """ Return list of all members ids from MongoDB """
    return list(members_collection.find({}, {'id': 1}))

