from datetime import datetime

from pymongo import MongoClient
from bson.json_util import dumps, loads


class Model:
	def __init__(self, request):
		self.db = MongoClient('localhost', 27017).test_database
		self.request = loads(request)


	def execute(self):
		if self.request['model'] == 'all':
			return self.getAll()
		elif self.request['model'] == 'message':
			return self.postMessage()


	def getAll(self):
		groups = loads(dumps(self.db.groups.find()))
		messages = loads(dumps(self.db.messages.find()))

		return self.__response('all', {'groups': groups, 'messages': messages})


	def postMessage(self):
		pk = self.db.messages.insert_one({
			'body'    : self.request['body'],
			'groupId' : self.request['groupId'],
			'personId': self.request['personId'],
			'created' : datetime.now().strftime('%Y%m%d%H%M%S')
		}).inserted_id

		return self.__response('message', self.db.messages.find_one(pk))


	def __response(self, model, body):
		return dumps({'model': model, 'body': loads(dumps(body))})
