angular.module('NgApp', ['ngWebSocket', 'ngRoute'])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'group-template',
      controller: 'GroupController'
    })
    .when('/event/:groupId', {
      templateUrl: 'event-template',
      controller: 'EventController'
    })
    .when('/message/:groupId', {
      templateUrl: 'message-template',
      controller: 'MessageController'
    })
    .when('/schedule/:groupId', {
      templateUrl: 'schedule-template',
      controller: 'ScheduleController'
    })
    .when('/attendance/:groupId/:scheduleId', {
      templateUrl: 'attendance-template',
      controller: 'AttendanceController'
    })
    .when('/link/:groupId', {
      templateUrl: 'link-template',
      controller: 'LinkController'
    })
    .when('/comment/:groupId/:linkId', {
      templateUrl: 'comment-template',
      controller: 'CommentController'
    })
    .otherwise({
      redirectTo: '/'
    });
}])

.controller('SocketController', ['$scope', '$websocket', function SocketController($scope, $websocket) {
	var socket = $websocket('ws://localhost:8080/ws');

	socket.onMessage(function(r) {
    $scope.result = r.data;
  });

  $scope.send = function() {
    socket.send('hoge--');
  };
}])

.controller('GroupController', ['$scope', function GroupController($scope) {
  $scope.groups = 'group list';
}])

.controller('EventController', ['$scope', '$routeParams', function EventController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
}])

.controller('MessageController', ['$scope', '$routeParams', function MessageController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
}])

.controller('ScheduleController', ['$scope', '$routeParams', function ScheduleController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
}])

.controller('AttendanceController', ['$scope', '$routeParams', function AttendanceController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
  $scope.scheduleId = $routeParams.scheduleId;
}])

.controller('LinkController', ['$scope', '$routeParams', function LinkController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
}])

.controller('CommentController', ['$scope', '$routeParams', function CommentController($scope, $routeParams) {
  $scope.groupId = $routeParams.groupId;
  $scope.linkId = $routeParams.linkId;
}]);
