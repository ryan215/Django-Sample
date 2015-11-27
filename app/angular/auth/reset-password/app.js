'use strict';
define(['app'], function(app) {
    app.register.controller('reset-passwordCtrl', ['$resource','$scope', '$stateParams', 'rest',
    	function($resource, $scope, $stateParams) {
    		var AuthReset =  $resource('http://:url/accounts/reset-password', {
                url: $scope.restURL
            });

    		$scope.user = {
    			email: $stateParams.email,
    			change_password_token: $stateParams.change_password_token,
				password: '',
				password2: ''
			};
	
			$scope.submit = function() {
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();
				$scope.authToken = AuthReset.save($scope.user, function() {
					window.location = '/#/login';
				},function(error) {
					$scope.message = error.data;
				});
			}
	}]);
});