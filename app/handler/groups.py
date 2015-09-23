import tornado.web


class GroupsHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.render('groups.html', personId = self.get_argument('personId'))
