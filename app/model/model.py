from datetime import datetime
from collections import OrderedDict

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads


class Model:
	def __init__(self, request, personId):
		self.db = MongoClient('localhost', 27017).test_database
		self.request = loads(request)
		self.personId = personId


	def execute(self):
		return getattr(self, '%s%s' % (self.request['method'], self.request['action'].capitalize()))()


	def getGroups(self):
		def join(group):
			groupId = group['_id'].__str__()
			group['unread'] = self.db.events.find({'groupId': groupId}).count()

			return group

		groups = [join(group) for group in self.db.groups.find()]

		return self.response('get', 'groups', groups)


	def getContent(self):
		groupId = self.request['groupId']
		group = self.db.groups.find_one({'_id': ObjectId(groupId)})
		messages = self.db.messages.find({'groupId': groupId})

		return self.response('get', 'content', {'group': group, 'messages': messages})


	def postMessage(self):
		pk = self.db.messages.insert_one({
			'body'    : self.request['body'],
			'groupId' : self.request['groupId'],
			'personId': self.personId,
			'created' : datetime.now().strftime('%Y/%m/%d %H:%M:%S')
		}).inserted_id

		return self.response('post', 'message', self.db.messages.find_one(pk))


	def response(self, method, action, body):
		return dumps({'method': method, 'action': action, 'body': body})
