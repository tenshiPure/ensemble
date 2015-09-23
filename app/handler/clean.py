# -*- coding: utf-8 -*-

import tornado.web

from pymongo import MongoClient


class CleanHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		client = MongoClient('localhost', 27017)
		client.drop_database('test_database')

		db = client.test_database
		db.groups.insert_one({'name': u'東京シティブラスオルケスター'})
		db.groups.insert_one({'name': u'伊藤マリーンズ'})

		db.messages.insert_one({'body': u'おはよう'})
		db.messages.insert_one({'body': u'こんにちは'})
		db.messages.insert_one({'body': u'こんばんは'})

		self.redirect('groups/?personId=1')
