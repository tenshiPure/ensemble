from pymongo import MongoClient
from bson.json_util import dumps, loads

from model.base import Base

class Message(Base):
	def getAll(self):
		return dumps(self.db.posts.find())


	def post(self):
		pk = self.db.posts.insert_one(self.toRow()).inserted_id
		return dumps(self.db.posts.find_one(pk))


	def toRow(self):
		return {'text': self.request['text'], 'author': self.request['author']}
