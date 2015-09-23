import tornado.web


class GroupHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render('group.html', personId = self.get_argument('personId'))
