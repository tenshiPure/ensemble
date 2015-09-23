angular.module('GroupApp', ['ngWebSocket']).factory('socket', function($websocket) {
	var dataStream = $websocket('ws://localhost:8080/group-ws?personId=' + getPersonId());

	var messages = [];

	dataStream.onMessage(function(message) {
    var json = JSON.parse(message.data);

		if (json['header']['status'] === 'ok') {
      if (json['header']['model'] == 'all') {
        for (message of json['body']['messages'])
          messages.push(message);
      }

      if (json['header']['model'] == 'message')
        messages.push(json['body']);
		}
	});

	var methods = {
		messages: messages,
		getAll: function() {
			dataStream.send(baseGetParams('all', getPersonId(), {}));
		},
		postMessage: function() {
			dataStream.send(basePostParams('message', '', { body: $('#message-body').val() }));
		},
	};

	return methods;

}).controller('MainController', ['$scope', 'socket', function ($scope, socket) {
  socket.getAll();
	$scope.socket = socket;

}]);

baseGetParams = function(model, personId, others) {
  return baseParams('get', model, personId, others);
};

basePostParams = function(model, personId, others) {
  return baseParams('post', model, personId, others);
};

baseParams = function(action, model, personId, others) {
  return JSON.stringify($.extend({ action: action, model: model, personId: personId }, others));
};

getPersonId = function() {
  return $('#person-id').val();
};
