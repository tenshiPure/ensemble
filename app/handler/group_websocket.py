import tornado.websocket

from client import Clients
import dispatcher


clients = Clients()


class GroupWebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		self.personId = self.get_argument('personId')
		clients.append(self)


	def on_close(self):
		clients.remove(self)


	def on_message(self, request):
		model = dispatcher.getModel(request)
		response = model.call()
		clients.send(request, response)
