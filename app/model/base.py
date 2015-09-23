from pymongo import MongoClient
from bson.json_util import dumps, loads


class Base:
	def __init__(self, request):
		self.db = MongoClient('localhost', 27017).test_database
		self.request = loads(request)


	def call(self):
		if self.request['action'] == 'get':
			return self.getAll()

		elif self.request['action'] == 'post':
			return self.post()


	def createResponse(self, model, cursor):
		return dumps({'header': {'status': 'ok', 'model': model}, 'body': loads(dumps(cursor))})
