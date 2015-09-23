angular.module('App', ['ngWebSocket']).factory('socket', function($websocket) {
	var dataStream = $websocket('ws://localhost:8080/ws');

	var messages = [];

	dataStream.onMessage(function(message) {
		messages.push(JSON.parse(message.data));
	});

	var methods = {
		messages: messages,
		getMessages: function() {
			dataStream.send(JSON.stringify({ action: 'get', model: 'message' }));
		},
		postMessage: function() {
			dataStream.send(JSON.stringify({ action: 'post', model: 'message', author: $('#author').val(), text: $('#text').val() }));
		},
	};

	return methods;

}).controller('MainController', ['$scope', 'socket', function ($scope, socket) {
	$scope.socket = socket;

}]);
