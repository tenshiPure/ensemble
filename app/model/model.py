from datetime import datetime

from pymongo import MongoClient
from bson.json_util import dumps, loads


class Model:
	def __init__(self, request):
		self.db = MongoClient('localhost', 27017).test_database
		self.request = loads(request)


	def execute(self):
		if self.request['model'] == 'groups':
			return self.getGroups()
		elif self.request['model'] == 'message':
			return self.postMessage()


	def getGroups(self):
		groups = {}
		for group in loads(dumps(self.db.groups.find())):
			pk = str(group['_id'])
			events = self.db.events.find({'groupId': pk})
			groups[pk] = {'name': group['name'], 'events': events, 'messages': []}

		return self.__response('groups', groups)


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
