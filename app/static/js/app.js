angular.module('App', ['ngWebSocket']).factory('socket', function($websocket, $http) {
	var dataStream = $websocket('ws://localhost:8080/ws');

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
		getAll: function(mode) {
			dataStream.send(JSON.stringify({ mode: mode, action: 'get', model: 'all' }));
		},
		postMessage: function(mode) {
			dataStream.send(JSON.stringify({ mode: mode, action: 'post', model: 'message', body: $('#message-body').val() }));
		},
	};

	return methods;

}).controller('MainController', ['$scope', '$http', 'socket', function ($scope, $http, socket) {
  socket.getAll('init');
	$scope.socket = socket;

}]);
