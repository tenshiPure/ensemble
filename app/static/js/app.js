angular.module('App', ['ngWebSocket', 'ngRoute'])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'view?name=groups',
      controller: 'GroupsController'
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
      if (json['action'] == 'groups') {
        $scope.groups = json['body'];
      }
      if (json['action'] == 'content') {
        $scope.content = json['body'];
      }
    }

    if (json['method'] == 'post') {
      if (json['action'] == 'message')
        $scope.content.messages.push(json['body']);
    }
  });

  $scope.send = function(method, action, others) {
    json = JSON.stringify(angular.extend({method: method, action: action}, others));
    $scope.socket.send(json);
  };
}])

.controller('GroupsController', ['$scope', '$routeParams', function GroupsController($scope, $routeParams) {
  $scope.send('get', 'groups', {});
}])

.controller('MessageController', ['$scope', '$routeParams', function MessageController($scope, $routeParams) {
  $scope.send('get', 'content', {groupId: $routeParams.groupId});

  $scope.post = function(form, body) {
    $scope.send('post', 'message', {groupId: $scope.content.group._id.$oid, body: body});
    form.body = '';
  };
}]);
