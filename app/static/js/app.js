angular.module('App', ['ngWebSocket', 'ngRoute'])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'view?name=group',
      controller: 'GroupController'
    })
    .when('/message/:groupId', {
      templateUrl: 'view?name=message',
      controller: 'MessageController'
    })
    .otherwise({
      redirectTo: '/'
    });
}])

.controller('RootController', ['$scope', '$websocket', '$filter', function RootController($scope, $websocket, $filter) {
  $scope.isCurrentTab = function(current) {
    return location.hash.indexOf(current) !== -1;
  };

  $scope.format = function(string) {
    var date = new Date(Date.parse(string));
    return $filter('date')(date, 'MM/dd HH:mm:ss');
  };

  $scope.personId = '1';
  $scope.groups = [];
  $scope.content = {};

	$scope.socket = $websocket('ws://localhost:8080/ws');

	$scope.socket.onMessage(function(r) {
    json = JSON.parse(r.data);

    if (json['method'] == 'get') {
    }

    if (json['method'] == 'post') {
    }
  });
}])

.controller('GroupController', ['$scope', '$routeParams', function GroupController($scope, $routeParams) {
  $scope.socket.send(JSON.stringify({method: 'get', model: 'group', personId: $scope.personId}));
}])

.controller('MessageController', ['$scope', '$routeParams', function MessageController($scope, $routeParams) {
  $scope.post = function(form, body) {
    $scope.socket.send(JSON.stringify({method: 'post', model: 'message', groupId: $scope.content.groupId, personId: $scope.personId, body: body}));
    form.body = '';
  };
}]);
