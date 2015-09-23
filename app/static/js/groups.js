angular.module('GroupsApp', ['ngWebSocket']).factory('socket', function($websocket) {
	var dataStream = $websocket('ws://localhost:8080/groups-ws?personId=' + getPersonId());

	var groups = [];

	dataStream.onMessage(function(message) {
    var json = JSON.parse(message.data);

		if (json['header']['status'] === 'ok') {
      if (json['header']['model'] == 'group') {
        for (group of json['body'])
          groups.push(group);
      }
		}
	});

	var methods = {
		groups: groups,
		getGroups: function() {
			dataStream.send(baseGetParams('group', getPersonId(), {}));
		},
	};

	return methods;

}).controller('MainController', ['$scope', 'socket', function ($scope, socket) {
  socket.getGroups();
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
