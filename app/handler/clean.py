# -*- coding: utf-8 -*-

from datetime import datetime

import tornado.web

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

from model.model import Model


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

		self.execute(person1, {'method': 'post', 'action': 'message', 'groupId': group1, 'body': u'おはよう'})
		self.execute(person1, {'method': 'post', 'action': 'message', 'groupId': group1, 'body': u'こんにちは'})
		self.execute(person1, {'method': 'post', 'action': 'message', 'groupId': group1, 'body': u'こんばんは'})
		self.execute(person1, {'method': 'post', 'action': 'message', 'groupId': group2, 'body': u'おっす'})

		schedule1 = self.execute(person1, {'method': 'post', 'action': 'schedule', 'groupId': group1, 'day': u'2015-09-28', 'place': '高橋区民センター', 'note': '指揮者不在のため、合奏はありません。'})
		schedule2 = self.execute(person1, {'method': 'post', 'action': 'schedule', 'groupId': group1, 'day': u'2015-10-05', 'place': '山田市営ホール',   'note': ''})

		self.execute(person1, {'method': 'post', 'action': 'attendance', 'groupId': group1, 'scheduleId': schedule1, 'choice': u'1', 'note': ''})
 		self.execute(person2, {'method': 'post', 'action': 'attendance', 'groupId': group1, 'scheduleId': schedule1, 'choice': u'2', 'note': '15時ごろから参加します'})

 		self.redirect('/login')


	def execute(self, personId, data):
		result = Model(personId = personId, request = dumps(data)).execute()
		return loads(result)['body']['_id'].__str__()
