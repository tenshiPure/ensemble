angular.module('GroupApp', ['ngWebSocket']).factory('socket', function($websocket) {
	var dataStream = $websocket('ws://localhost:8080/group-ws?groupId=' + getGroupId() + '&personId=' + getPersonId());

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
			dataStream.send(baseGetParams('all', getGroupId(), getPersonId(), {}));
		},
		postMessage: function() {
			dataStream.send(basePostParams('message', getGroupId(), getPersonId(), { body: $('#message-body').val() }));
		},
	};

	return methods;

}).controller('MainController', ['$scope', 'socket', function ($scope, socket) {
  socket.getAll();
	$scope.socket = socket;

}]);

baseGetParams = function(model, groupId, personId, others) {
  return baseParams('get', model, groupId, personId, others);
};

basePostParams = function(model, groupId, personId, others) {
  return baseParams('post', model, groupId, personId, others);
};

baseParams = function(action, model, groupId, personId, others) {
  return JSON.stringify($.extend({ action: action, model: model, groupId: groupId, personId: personId }, others));
};

getGroupId = function() {
  return $('#group-id').val();
};

getPersonId = function() {
  return $('#person-id').val();
};
