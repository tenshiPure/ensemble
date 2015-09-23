from bson.json_util import dumps, loads

from model.base import Base


class All(Base):
	def getAll(self):
		groups = loads(dumps(self.db.groups.find()))
		messages = loads(dumps(self.db.messages.find()))

		return self.createResponse('all', {'groups': groups, 'messages': messages})
