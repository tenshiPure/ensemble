from bson.json_util import loads

from model.message import Message

def getModel(request):
	models = {'message': Message}

	return models[loads(request)['model']](request)
