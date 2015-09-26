angular.module('App', ['ngWebSocket', 'ngRoute'])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'view?name=group',
      controller: 'GroupController'
    })
    .when('/event/:groupId/:personId', {
      templateUrl: 'view?name=event',
      controller: 'EventController'
    })
    .when('/message/:groupId/:personId', {
      templateUrl: 'view?name=message',
      controller: 'MessageController'
    })
    .when('/schedule/:groupId/:personId', {
      templateUrl: 'view?name=schedule',
      controller: 'ScheduleController'
    })
    .when('/attendance/:groupId/:personId/:scheduleId', {
      templateUrl: 'view?name=attendance',
      controller: 'AttendanceController'
    })
    .when('/link/:groupId/:personId', {
      templateUrl: 'view?name=link',
      controller: 'LinkController'
    })
    .when('/comment/:groupId/:personId/:linkId', {
      templateUrl: 'view?name=comment',
      controller: 'CommentController'
    })
    .otherwise({
      redirectTo: '/'
    });
}])

.controller('RootController', ['$scope', '$websocket', function RootController($scope, $websocket) {
  $scope.data = {};

	$scope.socket = $websocket('ws://localhost:8080/ws');

	$scope.socket.onMessage(function(r) {
    json = JSON.parse(r.data);
    if (json['method'] == 'get') {
      if (json['model'] == 'group')
        $scope.data = $.extend(true, $scope.data, json['body']);
      if (json['model'] == 'message')
        $scope.data[json['groupId']]['messages'] = json['body'];
    }

    if (json['method'] == 'post') {
      if (json['model'] == 'message')
        $scope.data[json['groupId']]['messages'].push(json['body']);
    }
  });
}])

.controller('GroupController', ['$scope', '$routeParams', function GroupController($scope, $routeParams) {
  $scope.socket.send(JSON.stringify({method: 'get', model: 'group', personId: $routeParams.personId}));
}])

.controller('EventController', ['$scope', '$location', '$routeParams', function EventController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
}])

.controller('MessageController', ['$scope', '$location', '$routeParams', function MessageController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;

  $scope.socket.send(JSON.stringify({method: 'get', model: 'message', groupId: $routeParams.groupId, personId: $routeParams.personId}));

  $scope.post = function(body) {
    $scope.socket.send(JSON.stringify({method: 'post', model: 'message', groupId: $routeParams.groupId, personId: $routeParams.personId, body: body}));
  };
}])

.controller('ScheduleController', ['$scope', '$location', '$routeParams', function ScheduleController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
}])

.controller('AttendanceController', ['$scope', '$location', '$routeParams', function AttendanceController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
}])

.controller('LinkController', ['$scope', '$location', '$routeParams', function LinkController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
}])

.controller('CommentController', ['$scope', '$location', '$routeParams', function CommentController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
}]);
