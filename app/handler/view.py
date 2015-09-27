import tornado.web


class ViewHandler(tornado.web.RequestHandler):
	def get(self):
		name = self.get_argument('name')
		self.render('view/%s.html' % name)
