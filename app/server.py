import os.path

import tornado.ioloop
import tornado.web

from handler.ng import NgHandler
from handler.socket import SocketHandler
from handler.template import TemplateHandler
from handler.groups import GroupsHandler
from handler.groups_websocket import GroupsWebSocketHandler
from handler.group import GroupHandler
from handler.group_websocket import GroupWebSocketHandler
from handler.clean import CleanHandler


app = tornado.web.Application(
	[
		(r'/ng', NgHandler),
		(r'/ws', SocketHandler),
		(r'/template', TemplateHandler),
		(r'/groups', GroupsHandler),
		(r'/groups-ws', GroupsWebSocketHandler),
		(r'/group', GroupHandler),
		(r'/group-ws', GroupWebSocketHandler),
		(r'/clean', CleanHandler),
	],
		template_path = os.path.join(os.getcwd(), 'template'),
		static_path = os.path.join(os.getcwd(), 'static'),
	)


if __name__ == '__main__':
	app.listen(8080)
	tornado.ioloop.IOLoop.instance().start()
