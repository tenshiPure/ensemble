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


	def send(self, response):
		[val.write_message(response) for val in self.vals]
