import tornado.web

from pymongo import MongoClient


class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_cookie('sid')

		self.redirect('/login')
