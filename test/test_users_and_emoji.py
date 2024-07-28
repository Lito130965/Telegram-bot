import unittest
import json
import pymongo.database
from pymongo.mongo_client import MongoClient
from mongo.mongoDB import insert_member_to_db, set_emoji_to_user, get_all_members_from_db, get_all_members_id_from_db
import random


class TestUsersAndEmoji(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient('mongodb://localhost')
        cls.telegram_db = cls.client.telegramDB
        cls.members_collection = cls.telegram_db.members
        with open('test/members_example.json') as file:
            cls.members = json.loads(file.read())
            #cls.members = file.read()

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def setUp(self):
        self.members_collection.drop()

    def tearDown(self):
        self.members_collection.drop()

    def test_insert_member_to_db(self):
        """ Testing to insert json document to MongoDB """
        member = self.members[random.randrange(len(self.members))]
        insert_member_to_db(member)
        self.assertEqual(self.members_collection.count_documents({}), 1)
        insert_member_to_db({'id': '444444', 'emoji': 'O'})
        self.assertEqual(self.members_collection.count_documents({}), 2)

    def test_set_emoji_to_user(self):
        """ Testing to add or change user emoji in MongoDB """
        self.members_collection.insert_many(self.members)
        ids = self.members_collection.find({}, {'id': 1})
        id_list = [id['id'] for id in ids]
        id_rand = random.choice(id_list)
        set_emoji_to_user(id_rand, 'T')
        self.assertEqual(self.members_collection.find_one({'id': id_rand})['emoji'], 'T')
        id_rand = random.choice(id_list)
        set_emoji_to_user(id_rand, 'T')
        self.assertEqual(self.members_collection.find_one({'id': id_rand})['emoji'], 'T')

    def test_get_all_members_from_db(self):
        """ Testing to get all documents from MongoDB collection """
        self.members_collection.insert_many(self.members)
        self.assertEqual(len(get_all_members_from_db()), 3)
        insert_member_to_db({'id': '444444', 'emoji': 'O'})
        self.assertEqual(len(get_all_members_from_db()), self.members_collection.count_documents({}))

    def test_get_all_members_id_from_db(self):
        self.members_collection.insert_many(self.members)
        self.assertEqual(len(get_all_members_id_from_db()), 3)
        insert_member_to_db({'id': '444444', 'emoji': 'O'})
        self.assertEqual(len(get_all_members_id_from_db()), self.members_collection.count_documents({}))
