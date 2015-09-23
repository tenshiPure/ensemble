angular.module('App', ['ngWebSocket']).factory('socket', function($websocket, $http) {
	var dataStream = $websocket('ws://localhost:8080/ws?personId=' + getPersonId());

	var groups = [];
	var messages = [];

	dataStream.onMessage(function(message) {
    var json = JSON.parse(message.data);

		if (json['header']['status'] === 'ok') {
      if (json['header']['model'] == 'all') {
        for (group of json['body']['groups'])
          groups.push(group);
        for (message of json['body']['messages'])
          messages.push(message);
      }

      if (json['header']['model'] == 'group')
        groups.push(json['body']);

      if (json['header']['model'] == 'message')
        messages.push(json['body']);
		}
	});

	var methods = {
		groups: groups,
		messages: messages,
		getAll: function() {
			dataStream.send(baseGetParams('all', getPersonId(), {}));
		},
		postMessage: function() {
			dataStream.send(basePostParams('message', '', { body: $('#message-body').val() }));
		},
	};

	return methods;

}).controller('MainController', ['$scope', '$http', 'socket', function ($scope, $http, socket) {
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
