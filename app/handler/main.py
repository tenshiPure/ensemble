import tornado.web


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		if self.get_secure_cookie('sid') is None:
			self.redirect('/login')

		self.render('main.html')
