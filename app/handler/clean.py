# -*- coding: utf-8 -*-

from datetime import datetime

import tornado.web

from pymongo import MongoClient
from bson.objectid import ObjectId


class CleanHandler(tornado.web.RequestHandler):
	def get(self):
		client = MongoClient('localhost', 27017)
		client.drop_database('test_database')

		db = client.test_database
		now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

		group1 = db.groups.insert_one({'name': u'東京シティブラスオルケスター', 'icon': 'tcbo.jpg'}).inserted_id.__str__()
		group2 = db.groups.insert_one({'name': u'伊藤マリーンズ', 'icon': 'marines.jpg'}).inserted_id.__str__()

		person1 = db.persons.insert_one({'name': u'中原和夫', 'icon': 'person1.png'}).inserted_id.__str__()
		person2 = db.persons.insert_one({'name': u'足立悦子', 'icon': 'person2.png'}).inserted_id.__str__()

		message1 = db.messages.insert_one({'body': u'おはよう',         'created': now, 'groupId': group1, 'personId': person1}).inserted_id.__str__()
		message2 = db.messages.insert_one({'body': u'こんにちは',       'created': now, 'groupId': group1, 'personId': person2}).inserted_id.__str__()
		message3 = db.messages.insert_one({'body': u'こんばんは',       'created': now, 'groupId': group1, 'personId': person1}).inserted_id.__str__()
		message4 = db.messages.insert_one({'body': u'また別のおはよう', 'created': now, 'groupId': group2, 'personId': person2}).inserted_id.__str__()

		schedule1 = db.schedules.insert_one({'day': u'2015-09-28', 'place': u'高橋区民センター', 'note': u'指揮者不在のため、合奏はありません。', 'created': now, 'groupId': group1, 'personId': person1}).inserted_id.__str__()
		schedule2 = db.schedules.insert_one({'day': u'2015-10-05', 'place': u'山田市営ホール',   'note': u'', 'created': now, 'groupId': group1, 'personId': person1}).inserted_id.__str__()

		attendance1 = db.attendances.insert_one({'choice': u'1', 'note': u'',                       'created': now, 'scheduleId': schedule1, 'groupId': group1, 'personId': person1}).inserted_id.__str__()
		attendance2 = db.attendances.insert_one({'choice': u'2', 'note': u'15時ごろから参加します', 'created': now, 'scheduleId': schedule1, 'groupId': group1, 'personId': person2}).inserted_id.__str__()


		person = db.persons.find_one(ObjectId(person1))

		db.events.insert_one({'type': 'message',    'messageId':  message1,  'body': u'おはよう',   'created': now, 'groupId': group1, 'person': person})
		db.events.insert_one({'type': 'schedule',   'scheduleId': schedule1, 'day':  u'2015-09-28', 'created': now, 'groupId': group1, 'person': person})
		db.events.insert_one({'type': 'attendance', 'scheduleId': schedule1, 'attendanceId': attendance1, 'day':  u'2015-09-28', 'choice': '1', 'created': now, 'groupId': group1, 'person': person})

		self.redirect('/login')
