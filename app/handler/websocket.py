import tornado.websocket

from clients import Clients
from model.model import Model

clients = Clients()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		clients.append(self)


	def on_close(self):
		clients.remove(self)


	def on_message(self, request):
		model = Model(request)
		response = model.execute()
		clients.send(response)
