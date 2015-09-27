import tornado.web

from pymongo import MongoClient


class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		db = MongoClient('localhost', 27017).test_database
		persons = db.persons.find()

		options = ''.join(['<option value="%(_id)s">%(name)s</option>' % person for person in persons])

		self.write("""
			<form method="post">
				<select name="personId">
					%(options)s
				</select>
				<input type="submit" value="login">
			</form>
		""" % locals())

	def post(self):
		self.set_secure_cookie('sid', self.get_argument('personId'))

		self.redirect('/')
