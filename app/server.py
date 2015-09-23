import os.path

import tornado.ioloop
import tornado.web
import tornado.websocket

from client import Clients
import dispatcher

from model.message import Message


class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render("index.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		clients.append(self)


	def on_close(self):
		clients.remove(self)


	def on_message(self, request):
		model = dispatcher.getModel(request)
		response = model.call()
		clients.send(response)


app = tornado.web.Application(
	[
		(r"/", IndexHandler),
		(r"/ws", WebSocketHandler),
	],
		template_path = os.path.join(os.getcwd(), 'template'),
		static_path = os.path.join(os.getcwd(), 'static'),
	)


if __name__ == "__main__":
	clients = Clients()

	app.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
