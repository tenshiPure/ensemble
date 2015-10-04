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
		messages = [self.joinPerson(message) for message in self.db.messages.find({'groupId': groupId})]
		schedules = [schedule for schedule in self.db.schedules.find({'groupId': groupId})]

		return self.response('get', 'content', {'group': group, 'messages': messages, 'schedules': schedules})


	def getAttendances(self):
		scheduleId = self.request['scheduleId']
		schedule = self.db.schedules.find_one({'_id': ObjectId(scheduleId)})
		attendances = [self.joinPerson(attendance) for attendance in self.db.attendances.find({'scheduleId': scheduleId})]

		return self.response('get', 'attendances', {'schedule': schedule, 'attendances': attendances})


	def joinPerson(self, dic):
		personId = dic.pop('personId')
		person = self.db.persons.find_one(ObjectId(personId))
		dic['person'] = person

		return dic


	def postMessage(self):
		pk = self.db.messages.insert_one({
			'body'    : self.request['body'],
			'created' : datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
			'groupId' : self.request['groupId'],
			'personId': self.personId
		}).inserted_id

		return self.response('post', 'message', self.db.messages.find_one(pk))


	def postSchedule(self):
		pk = self.db.schedules.insert_one({
			'day'     : self.request['day'],
			'place'   : self.request['place'],
			'note'    : self.request['note'],
			'created' : datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
			'groupId' : self.request['groupId'],
			'personId': self.personId
		}).inserted_id

		return self.response('post', 'schedule', self.db.schedules.find_one(pk))


	def postAttendance(self):
		pk = self.db.attendances.insert_one({
			'choice'     : self.request['choice'],
			'note'       : self.request['note'],
			'created'    : datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
			'scheduleId' : self.request['scheduleId'],
			'groupId'    : self.request['groupId'],
			'personId'   : self.personId
		}).inserted_id

		return self.response('post', 'attendance', self.db.attendances.find_one(pk))


	def response(self, method, action, body):
		return dumps({'method': method, 'action': action, 'body': body})


	def responseWithGroupId(self, method, action, body):
		return dumps({'method': method, 'action': action, 'body': body, 'groupId': self.request['groupId']})
