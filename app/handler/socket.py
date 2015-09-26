import tornado.websocket


class SocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print 'open'


	def on_close(self):
		print 'close'


	def on_message(self, request):
		self.write_message('I get request: %s' % request)
