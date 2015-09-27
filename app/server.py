import os.path

import tornado.ioloop
import tornado.web

from handler.main import MainHandler
from handler.websocket import WebSocketHandler
from handler.include import IncludeHandler
from handler.view import ViewHandler
from handler.login import LoginHandler
from handler.logout import LogoutHandler
from handler.clean import CleanHandler


app = tornado.web.Application(
	[
		(r'/', MainHandler),
		(r'/ws', WebSocketHandler),
		(r'/include', IncludeHandler),
		(r'/view', ViewHandler),
		(r'/login', LoginHandler),
		(r'/logout', LogoutHandler),
		(r'/clean', CleanHandler),
	],
		template_path = os.path.join(os.getcwd(), 'template'),
		static_path = os.path.join(os.getcwd(), 'static'),
		cookie_secret = 'cookie secret',
	)


if __name__ == '__main__':
	app.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
