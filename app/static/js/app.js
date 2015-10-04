angular.module('App', ['ngWebSocket', 'ngRoute'])
.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'view?name=groups',
      controller: 'GroupsController'
    })
    .when('/event/:groupId', {
      templateUrl: 'view?name=event',
      controller: 'EventController'
    })
    .when('/message/:groupId', {
      templateUrl: 'view?name=message',
      controller: 'MessageController'
    })
    .when('/schedule/:groupId', {
      templateUrl: 'view?name=schedule',
      controller: 'ScheduleController'
    })
    .when('/attendance/:groupId/:scheduleId', {
      templateUrl: 'view?name=attendance',
      controller: 'AttendanceController'
    })
    .otherwise({
      redirectTo: '/'
    });
}])

.controller('RootController', ['$scope', '$websocket', '$filter', function($scope, $websocket, $filter) {
  $scope.isCurrentTab = function(current) {
    return location.hash.indexOf(current) !== -1;
  };

  $scope.format = function(string) {
    var date = new Date(Date.parse(string));
    return $filter('date')(date, 'MM/dd HH:mm:ss');
  };

  $scope.groups = [];
  $scope.content = {};
  $scope.subcontent = {};

	$scope.socket = $websocket('ws://localhost:8080/ws');

	$scope.socket.onMessage(function(r) {
    json = JSON.parse(r.data);

    if (json.method === 'get') {
      if (json.action === 'groups')
        $scope.groups = json.body;
      if (json.action === 'content')
        $scope.content = json.body;
      if (json.action === 'attendances') {
        $scope.subcontent.schedule = json.body.schedule;
        $scope.subcontent.attendances = json.body.attendances;
      }
    }

    if (json.method === 'post') {
      if (json.action === 'message' && isCurrentGroup($scope, json.body.message.groupId)) {
        $scope.content.messages.push(json.body.message);
        $scope.content.events.push(json.body.events);
      }
      if (json.action === 'schedule' && isCurrentGroup($scope, json.body.schedule.groupId)) {
        $scope.content.schedules.push(json.body);
      }
      if (json.action === 'attendance' && isCurrentAttendance($scope, json.body.attendance.scheduleId)) {
        $scope.subcontent.attendances.push(json.body);
      }
    }
  });

  $scope.send = function(method, action, others) {
    json = JSON.stringify(angular.extend({method: method, action: action}, others));
    $scope.socket.send(json);
  };
}])

.controller('GroupsController', ['$scope', function($scope) {
  $scope.send('get', 'groups', {});
}])

.controller('EventController', ['$scope', '$routeParams', '$location', function($scope, $routeParams, $location) {
  $scope.groupId = $routeParams.groupId;

  $scope.send('get', 'content', {groupId: $scope.groupId});
}])

.controller('MessageController', ['$scope', '$routeParams', '$location', function($scope, $routeParams, $location) {
  guard($location, $scope);

  $scope.groupId = $routeParams.groupId;

  $scope.post = function(form, body) {
    $scope.send('post', 'message', {groupId: $scope.groupId, body: body});
    form.body = '';
  };
}])

.controller('ScheduleController', ['$scope', '$routeParams', '$location', function($scope, $routeParams, $location) {
  guard($location, $scope);

  $scope.groupId = $routeParams.groupId;

  $scope.post = function(form, day, place, note) {
    $scope.send('post', 'schedule', {groupId: $scope.groupId, day: day, place: place, note: note});
    form.day = '';
    form.place = '';
    form.note = '';
  };
}])

.controller('AttendanceController', ['$scope', '$routeParams', '$location', function($scope, $routeParams, $location) {
  guard($location, $scope);

  $scope.groupId = $routeParams.groupId;

  $scope.send('get', 'attendances', {scheduleId: $routeParams.scheduleId});

  $scope.post = function(form, choice, note) {
    $scope.send('post', 'attendance', {groupId: $scope.groupId, choice: choice, note: note, scheduleId: $routeParams.scheduleId});
    form.choice = '';
    form.note = '';
  };
}]);


isCurrentGroup = function($scope, groupId) {
  return $scope.content.group._id.$oid === groupId;
};


isCurrentAttendance = function($scope, scheduleId) {
  return ($scope.subcontent.schedule !== undefined) && ($scope.subcontent.schedule._id.$oid === scheduleId);
};


guard = function($location, $scope) {
  if (Object.keys($scope.content).length === 0) { $location.path('/'); }
};
