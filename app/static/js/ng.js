angular.module('NgApp', ['ngRoute'])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'group-template',
      controller: 'GroupController'
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

.controller('GroupController', ['$scope', function GroupController($scope) {
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
