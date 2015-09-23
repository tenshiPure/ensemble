from bson.json_util import loads


class Clients:
	def __init__(self):
		self.vals = []


	def append(self, val):
		if val not in self.vals:
			self.vals.append(val)


	def remove(self, val):
		if val in self.vals:
			self.vals.remove(val)


	def send(self, request, response):
		personId = loads(request)['personId']

		if personId == '':
			[val.write_message(response) for val in self.vals]
		else:
			[val.write_message(response) for val in self.vals if val.personId == personId]
