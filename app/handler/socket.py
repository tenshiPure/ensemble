import tornado.websocket


clients = []


class SocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		if self not in clients:
			clients.append(self)


	def on_close(self):
		if self in clients:
			clients.remove(self)


	def on_message(self, request):
		from pymongo import MongoClient
		from bson.json_util import dumps, loads

		db = MongoClient('localhost', 27017).test_database
		request = loads(request)

		if request['model'] == 'message':
			from datetime import datetime
			pk = db.messages.insert_one({'body': request['body'], 'groupId': request['groupId'], 'personId': request['personId'], 'created': datetime.now().strftime('%Y%m%d%H%M%S')}).inserted_id
			res = dumps({'model': 'message', 'body': loads(dumps(db.messages.find_one(pk)))})
		elif request['model'] == 'all':
			groups = loads(dumps(db.groups.find()))
			messages = loads(dumps(db.messages.find()))
			res = dumps({'model': 'all', 'body': {'groups': groups, 'messages': messages}})

		[c.write_message(res) for c in clients]
