import tornado.web


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		personId = self.get_secure_cookie('sid')
		self.render('main.html', personId = personId)
