# -*- coding: utf-8 -*-

from datetime import datetime

import tornado.web

from pymongo import MongoClient


class CleanHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		client = MongoClient('localhost', 27017)
		client.drop_database('test_database')

		db = client.test_database
		group1 = db.groups.insert_one({'name': u'東京シティブラスオルケスター'}).inserted_id.__str__()
		group2 = db.groups.insert_one({'name': u'伊藤マリーンズ'}).inserted_id.__str__()

		now = datetime.now().strftime('%Y%m%d%H%M%S')
		db.messages.insert_one({'body': u'おはよう', 'created': now, 'groupId': group1, 'personId': '1'})
		db.messages.insert_one({'body': u'こんにちは', 'created': now, 'groupId': group1, 'personId': '1'})
		db.messages.insert_one({'body': u'こんばんは', 'created': now, 'groupId': group1, 'personId': '1'})
		db.messages.insert_one({'body': u'また別のおはよう', 'created': now, 'groupId': group2, 'personId': '1'})

		self.redirect('/')
