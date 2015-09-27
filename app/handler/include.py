import tornado.web


class IncludeHandler(tornado.web.RequestHandler):
	def get(self):
		name = self.get_argument('name')
		self.render('include/%s.html' % name)
