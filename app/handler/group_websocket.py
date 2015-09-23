import tornado.websocket

from group_client import Clients
import dispatcher


clients = Clients()


class GroupWebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		self.groupId = self.get_argument('groupId')
		self.personId = self.get_argument('personId')
		clients.append(self)


	def on_close(self):
		clients.remove(self)


	def on_message(self, request):
		model = dispatcher.getModel(request)
		response = model.call()
		clients.send(request, response)
