import tornado.websocket

from model import Model

clients = []


class SocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		if self not in clients:
			clients.append(self)


	def on_close(self):
		if self in clients:
			clients.remove(self)


	def on_message(self, request):
		model = Model(request)
		response = model.execute()

		[c.write_message(response) for c in clients]
