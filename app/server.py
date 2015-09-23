# -*- coding: utf-8 -*-

import os.path

import tornado.ioloop
import tornado.web
import tornado.websocket

from client import Clients
import dispatcher

from model.all import All


class CleanHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		from pymongo import MongoClient
		client = MongoClient('localhost', 27017)
		client.drop_database('test_database')

		db = client.test_database
		db.groups.insert_one({'name': u'東京シティブラスオルケスター'})
		db.groups.insert_one({'name': u'伊藤マリーンズ'})

		db.messages.insert_one({'body': u'おはよう'})
		db.messages.insert_one({'body': u'こんにちは'})
		db.messages.insert_one({'body': u'こんばんは'})

		self.redirect('/?personId=1')


class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render('index.html', personId = self.get_argument('personId'))


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		self.personId = self.get_argument('personId')
		clients.append(self)


	def on_close(self):
		clients.remove(self)


	def on_message(self, request):
		model = dispatcher.getModel(request)
		response = model.call()
		clients.send(request, response)


app = tornado.web.Application(
	[
		(r'/', IndexHandler),
		(r'/clean', CleanHandler),
		(r'/ws', WebSocketHandler),
	],
		template_path = os.path.join(os.getcwd(), 'template'),
		static_path = os.path.join(os.getcwd(), 'static'),
	)


if __name__ == '__main__':
	clients = Clients()

	app.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
