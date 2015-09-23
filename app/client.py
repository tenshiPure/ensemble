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
		for val in self.vals:
			val.write_message(response)
