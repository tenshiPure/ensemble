from bson.json_util import loads

from model.group import Group
from model.person import Person
from model.message import Message

def getModel(request):
	models = {'group': Group, 'person': Person, 'message': Message}

	return models[loads(request)['model']](request)
