from datetime import datetime
from collections import OrderedDict

import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads


class Model:
	def __init__(self, request):
		self.db = MongoClient('localhost', 27017).test_database
		self.request = loads(request)


	def execute(self):
		if self.request['method'] == 'get':
			if self.request['model'] == 'group':
				return self.getGroups()
			if self.request['model'] == 'message':
				return self.getMessages()

		if self.request['method'] == 'post':
			if self.request['model'] == 'message':
				return self.postMessage()


	def getGroups(self):
		groups = OrderedDict()
		for group in loads(dumps(self.db.groups.find())):
			pk = str(group['_id'])
			events = self.db.events.find({'groupId': pk}).sort('_id', pymongo.ASCENDING)
			groups[pk] = {'name': group['name'], 'events': events, 'messages': []}

		return self.__response('get', 'group', groups)


	def getMessages(self):
		return self.__responseWithGroupId('get', 'message', self.db.messages.find({'groupId': self.request['groupId']}).sort('created', pymongo.ASCENDING))


	def postMessage(self):
		pk = self.db.messages.insert_one({
			'body'    : self.request['body'],
			'groupId' : self.request['groupId'],
			'personId': self.request['personId'],
			'created' : datetime.now().strftime('%Y%m%d%H%M%S')
		}).inserted_id

		return self.__responseWithGroupId('post', 'message', self.db.messages.find_one(pk))


	def __response(self, method, model, body):
		return dumps({'method': method, 'model': model, 'body': body})


	def __responseWithGroupId(self, method, model, body):
		return dumps({'method': method, 'model': model, 'groupId': self.request['groupId'], 'body': loads(dumps(body))})
