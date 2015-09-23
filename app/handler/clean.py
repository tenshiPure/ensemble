# -*- coding: utf-8 -*-

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

		db.messages.insert_one({'body': u'おはよう', 'groupId': group1})
		db.messages.insert_one({'body': u'こんにちは', 'groupId': group1})
		db.messages.insert_one({'body': u'こんばんは', 'groupId': group1})
		db.messages.insert_one({'body': u'また別のおはよう', 'groupId': group2})

		self.redirect('groups?personId=1')
