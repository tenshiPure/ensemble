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
		if self.request['method'] == 'get':
			if self.request['model'] == 'group':
				return self.getGroups()
			if self.request['model'] == 'message':
				return self.getMessages()
			if self.request['model'] == 'schedule':
				return self.getSchedules()
			if self.request['model'] == 'attendance':
				return self.getAttendances()

		if self.request['method'] == 'post':
			if self.request['model'] == 'message':
				return self.postMessage()
			if self.request['model'] == 'schedule':
				return self.postSchedule()
			if self.request['model'] == 'attendance':
				return self.postAttendance()


	def getGroups(self):
		groups = OrderedDict()
		for group in loads(dumps(self.db.groups.find())):
			groupId = str(group['_id'])
			events = self.db.events.find({'groupId': groupId}).sort('_id', pymongo.ASCENDING)
			groups[groupId] = {'name': group['name'], 'events': events, 'messages': [], 'schedules': [], 'attendances': []}

		return self.__response('get', 'group', groups)


	def getMessages(self):
		messages = self.db.messages.find({'groupId': self.request['groupId']}).sort('_id', pymongo.DESCENDING)

		def join(message):
			personId = message['personId']
			person = self.db.persons.find_one({'_id': ObjectId(personId)})
			message['person'] = person
			return message

		return self.__responseWithGroupId('get', 'message', map(join, messages))


	def getSchedules(self):
		schedules = self.db.schedules.find({'groupId': self.request['groupId']}).sort('_id', pymongo.DESCENDING)

		def join(schedule):
			personId = schedule['personId']
			person = self.db.persons.find_one({'_id': ObjectId(personId)})
			schedule['person'] = person
			return schedule

		return self.__responseWithGroupId('get', 'schedule', map(join, schedules))


	def getAttendances(self):
		attendances = self.db.attendances.find({'groupId': self.request['groupId'], 'scheduleId': self.request['scheduleId']}).sort('_id', pymongo.DESCENDING)

		def join(attendance):
			personId = attendance['personId']
			person = self.db.persons.find_one({'_id': ObjectId(personId)})
			attendance['person'] = person
			return attendance

		return self.__responseWithGroupId('get', 'attendance', map(join, attendances))


	def postMessage(self):
		pk = self.db.messages.insert_one({
			'body'    : self.request['body'],
			'groupId' : self.request['groupId'],
			'personId': self.request['personId'],
			'created' : datetime.now().strftime('%Y/%m/%d %H:%M:%S')
		}).inserted_id

		return self.__responseWithGroupId('post', 'message', self.db.messages.find_one(pk))


	def postSchedule(self):
		pk = self.db.schedules.insert_one({
			'day'     : self.request['day'],
			'place'   : self.request['place'],
			'note'    : self.request['note'],
			'created' : datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
			'groupId' : self.request['groupId'],
			'personId': self.request['personId'],
		}).inserted_id

		return self.__responseWithGroupId('post', 'schedule', self.db.schedules.find_one(pk))


	def postAttendance(self):
		saved = self.db.attendances.find_one({'scheduleId': self.request['scheduleId'], 'groupId': self.request['groupId'], 'personId': self.request['personId']})

		if saved is None:
			pk = self.db.attendances.insert_one({
				'choice'     : self.request['choice'],
				'note'       : self.request['note'],
				'created'    : datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
				'scheduleId' : self.request['scheduleId'],
				'groupId'    : self.request['groupId'],
				'personId'   : self.request['personId'],
			}).inserted_id

			return self.__responseWithGroupId('post', 'attendance', self.db.attendances.find_one(pk))

		else:
			pk = saved['_id']
			saved['choice'] = self.request['choice']
			saved['note'] = self.request['note']
			saved['created'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

			self.db.attendances.replace_one({'_id': pk}, saved)

			return self.getAttendances()


	def __response(self, method, model, body):
		return dumps({'method': method, 'model': model, 'personId': self.personId, 'body': body})


	def __responseWithGroupId(self, method, model, body):
		return dumps({'method': method, 'model': model, 'groupId': self.request['groupId'], 'body': loads(dumps(body))})
