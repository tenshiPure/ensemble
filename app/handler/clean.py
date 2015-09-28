# -*- coding: utf-8 -*-

from datetime import datetime

import tornado.web

from pymongo import MongoClient


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

		db.messages.insert_one({'body': u'おはよう',         'created': now, 'groupId': group1, 'personId': person1})
		db.messages.insert_one({'body': u'こんにちは',       'created': now, 'groupId': group1, 'personId': person2})
		db.messages.insert_one({'body': u'こんばんは',       'created': now, 'groupId': group1, 'personId': person1})
		db.messages.insert_one({'body': u'また別のおはよう', 'created': now, 'groupId': group2, 'personId': person2})

		db.schedules.insert_one({'day': u'2015-09-28', 'place': u'高橋区民センター', 'note': u'指揮者不在のため、合奏はありません。', 'created': now, 'groupId': group1, 'personId': person1})
		db.schedules.insert_one({'day': u'2015-10-05', 'place': u'山田市営ホール',   'note': u'', 'created': now, 'groupId': group1, 'personId': person1})

		db.events.insert_one({'body': u'新規イベント1', 'created': now, 'groupId': group1})
		db.events.insert_one({'body': u'新規イベント2', 'created': now, 'groupId': group1})
		db.events.insert_one({'body': u'新規イベント3', 'created': now, 'groupId': group2})

		self.redirect('/')
