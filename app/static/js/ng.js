angular.module('NgApp', ['ngWebSocket', 'ngRoute'])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'group-template',
      controller: 'GroupController'
    })
    .when('/event/:groupId/:personId', {
      templateUrl: 'event-template',
      controller: 'EventController'
    })
    .when('/message/:groupId/:personId', {
      templateUrl: 'message-template',
      controller: 'MessageController'
    })
    .when('/schedule/:groupId/:personId', {
      templateUrl: 'schedule-template',
      controller: 'ScheduleController'
    })
    .when('/attendance/:groupId/:personId/:scheduleId', {
      templateUrl: 'attendance-template',
      controller: 'AttendanceController'
    })
    .when('/link/:groupId/:personId', {
      templateUrl: 'link-template',
      controller: 'LinkController'
    })
    .when('/comment/:groupId/:personId/:linkId', {
      templateUrl: 'comment-template',
      controller: 'CommentController'
    })
    .otherwise({
      redirectTo: '/'
    });
}])

.controller('SocketController', ['$scope', '$websocket', function SocketController($scope, $websocket) {
	$scope.socket = $websocket('ws://localhost:8080/ws');

	$scope.socket.onMessage(function(r) {
    json = JSON.parse(r.data);
    if (json['model'] == 'all')
      $scope.data = json['body'];
    if (json['model'] == 'message')
      $scope.data['messages'].push(json['body']);
  });
}])

.controller('GroupController', ['$scope', function GroupController($scope) {
}])

.controller('EventController', ['$scope', '$routeParams', function EventController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;

  $scope.socket.send(JSON.stringify({model: 'all', groupId: $routeParams.groupId, personId: $routeParams.personId}));
}])

.controller('MessageController', ['$scope', '$routeParams', function MessageController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;

  $scope.post = function(body) {
    $scope.socket.send(JSON.stringify({model: 'message', groupId: $routeParams.groupId, personId: $routeParams.personId, body: body}));
  };
}])

.controller('ScheduleController', ['$scope', '$routeParams', function ScheduleController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
}])

.controller('AttendanceController', ['$scope', '$routeParams', function AttendanceController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
  $scope.scheduleId = $routeParams.scheduleId;
}])

.controller('LinkController', ['$scope', '$routeParams', function LinkController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
}])

.controller('CommentController', ['$scope', '$routeParams', function CommentController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
  $scope.personId = $routeParams.personId;
  $scope.linkId = $routeParams.linkId;
}]);
