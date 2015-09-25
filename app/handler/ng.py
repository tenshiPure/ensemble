import tornado.web


class NgHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render('ng.html')
