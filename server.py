import tornado.ioloop
import tornado.web
import tornado.websocket

from pymongo import MongoClient

from client import Clients


class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render("index.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		clients.append(self)


	def on_close(self):
		clients.remove(self)


	def on_message(self, message):
		clients.sendJson(db.posts.find())


app = tornado.web.Application([
	(r"/", IndexHandler),
	(r"/ws", WebSocketHandler),
])


if __name__ == "__main__":
	db = MongoClient('localhost', 27017).test_database

	clients = Clients()

	app.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
