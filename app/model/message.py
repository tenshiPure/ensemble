from datetime import datetime

from model.base import Base


class Message(Base):
	def getAll(self):
		return self.createResponse('message', self.db.messages.find())


	def post(self):
		pk = self.db.messages.insert_one(self.toRow()).inserted_id
		return self.createResponse('message', self.db.messages.find_one(pk))


	def toRow(self):
		return {'body': self.request['body'], 'groupId': self.request['groupId'], 'personId': self.request['personId'], 'created': datetime.now().strftime('%Y%m%d%H%M%S')}
