from bson.json_util import dumps, loads

from model.base import Base


class All(Base):
	def getAll(self):
		messages = loads(dumps(self.db.messages.find({'groupId': self.request['groupId']})))

		return self.createResponse('all', {'messages': messages})
