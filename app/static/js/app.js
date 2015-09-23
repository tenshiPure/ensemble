angular.module('App', ['ngWebSocket']).factory('socket', function($websocket) {
	var dataStream = $websocket('ws://localhost:8080/ws');

	var response = {groups: [], persons: []};

	dataStream.onMessage(function(message) {
		var json = JSON.parse(message.data);
		if (json['header']['status'] === 'ok') {
			response[json['header']['model']].push(json['body']);
		}
	});

	var methods = {
		response: response,
		getGroups: function() {
			dataStream.send(JSON.stringify({ action: 'get', model: 'group' }));
		},
		postGroup: function() {
			dataStream.send(JSON.stringify({ action: 'post', model: 'group', name: $('#group-name').val() }));
		},
		getPersons: function() {
			dataStream.send(JSON.stringify({ action: 'get', model: 'person' }));
		},
		postPerson: function() {
			dataStream.send(JSON.stringify({ action: 'post', model: 'person', name: $('#person-name').val(), icon: $('#person-icon').val() }));
		},
	};

	return methods;

}).controller('MainController', ['$scope', 'socket', function ($scope, socket) {
	$scope.socket = socket;

}]);
