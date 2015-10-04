import tornado.websocket

from bson.json_util import loads

from model.model import Model


clients = []


class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		if self not in clients:
			clients.append(self)


	def on_close(self):
		if self in clients:
			clients.remove(self)


	def on_message(self, request):
		personId = self.get_secure_cookie('sid')

		model = Model(request, personId)
		response = model.execute()

		if loads(request)['method'] == 'get':
			self.write_message(response)
		else:
			[client.write_message(response) for client in clients]
