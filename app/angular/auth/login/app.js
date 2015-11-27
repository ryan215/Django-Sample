'use strict';

define(['app'], function(app) {
    app.register.controller('loginCtrl', ['$state',"localStorageService","$resource","$scope", "rest", 'restricted',
    	function($state, localStorageService, $resource, $scope) {
    		var AuthToken =  $resource("https://:url/accounts/login", {
                url: $scope.restURL
            });
    		$scope.user = {
				email: '',
				password: ''
			};
			$scope.submit = function() {
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();
				$scope.authToken = AuthToken.save($scope.user, function() {
					localStorageService.add('Authorization', 'Token ' + $scope.authToken.token);
					localStorageService.add('rest_token', $scope.authToken.token);
					localStorageService.add('user_id', $scope.authToken.id);
					localStorageService.add('user_email', $scope.authToken.email);
                    localStorageService.add('user_img', $scope.authToken.img);
                    localStorageService.add('user_type', $scope.authToken.type);
                    $scope.restricted();
                    $state.go('home');
				},function(error) {
					$scope.message = error.data;
				});
			};
            $scope.closeAlert = function (error) {
                delete $scope.message[error];
            };
	}]);
});