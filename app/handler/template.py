import tornado.web


class TemplateHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		name = self.get_argument('name')
		self.render('%s.html' % name)
