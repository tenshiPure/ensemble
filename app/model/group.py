from model.base import Base

class Group(Base):
	def getAll(self):
		return self.createResponse('group', self.db.groups.find())


	def post(self):
		pk = self.db.groups.insert_one(self.toRow()).inserted_id
		return self.createResponse('group', self.db.groups.find_one(pk))


	def toRow(self):
		return {'name': self.request['name']}
