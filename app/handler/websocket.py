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
		personId = self.get_secure_cookie('sid')

		model = Model(request, personId)
		response = model.execute()
		clients.send(response)
