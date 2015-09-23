from model.base import Base

class Person(Base):
	def getAll(self):
		return self.createResponse('persons', self.db.persons.find())


	def post(self):
		pk = self.db.persons.insert_one(self.toRow()).inserted_id
		return self.createResponse('persons', self.db.persons.find_one(pk))


	def toRow(self):
		return {'name': self.request['name'], 'icon': self.request['icon']}
