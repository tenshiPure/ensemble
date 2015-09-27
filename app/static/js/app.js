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

.controller('RootController', ['$scope', '$websocket', '$filter', function RootController($scope, $websocket, $filter) {
  $scope.isCurrentTab = function(current) {
    return location.hash.indexOf(current) !== -1;
  };

  $scope.data = {};
  $scope.personId = '';

	$scope.socket = $websocket('ws://localhost:8080/ws');

	$scope.socket.onMessage(function(r) {
    json = JSON.parse(r.data);
    if (json['method'] == 'get') {
      if (json['model'] == 'group') {
        $scope.data = $.extend(true, $scope.data, json['body']);
        $scope.personId = json['personId'];
      }
      if (json['model'] == 'message')
        $scope.data[json['groupId']]['messages'] = json['body'];
    }

    if (json['method'] == 'post') {
      if (json['model'] == 'message')
        $scope.data[json['groupId']]['messages'].unshift(json['body']);
    }
  });

  $scope.format = function(string) {
    var date = new Date(Date.parse(string));
    return $filter('date')(date, 'MM/dd HH:mm:ss');
  };
}])

.controller('GroupController', ['$scope', '$routeParams', function GroupController($scope, $routeParams) {
  $scope.socket.send(JSON.stringify({method: 'get', model: 'group', personId: $routeParams.personId}));
}])

.controller('EventController', ['$scope', '$location', '$routeParams', function EventController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
}])

.controller('MessageController', ['$scope', '$location', '$routeParams', function MessageController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;

  $scope.socket.send(JSON.stringify({method: 'get', model: 'message', groupId: $routeParams.groupId, personId: $scope.personId}));

  $scope.post = function(form, body) {
    $scope.socket.send(JSON.stringify({method: 'post', model: 'message', groupId: $routeParams.groupId, personId: $scope.personId, body: body}));
    form.body = '';
  };
}])

.controller('ScheduleController', ['$scope', '$location', '$routeParams', function ScheduleController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
}])

.controller('AttendanceController', ['$scope', '$location', '$routeParams', function AttendanceController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
}])

.controller('LinkController', ['$scope', '$location', '$routeParams', function LinkController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
}])

.controller('CommentController', ['$scope', '$location', '$routeParams', function CommentController($scope, $location, $routeParams) {
  if (Object.keys($scope.data).length === 0) { $location.path('/'); return; }

  $scope.groupId = $routeParams.groupId;
}]);
