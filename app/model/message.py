from model.base import Base

class Message(Base):
	def getAll(self):
		return self.createResponse('message', self.db.messages.find())


	def post(self):
		pk = self.db.messages.insert_one(self.toRow()).inserted_id
		return self.createResponse('message', self.db.messages.find_one(pk))


	def toRow(self):
		return {'body': self.request['body']}
