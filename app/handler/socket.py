import tornado.websocket
import datetime


clients = []


class SocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print 'open'
		self.write_message('res open')
		if self not in clients:
			clients.append(self)


	def on_close(self):
		print 'close'
		self.write_message('res close')
		if self in clients:
			clients.remove(self)
		print clients


	def on_message(self, request):
		print request
		now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
		[c.write_message('I get request: %s at %s' % (request, now)) for c in clients]
