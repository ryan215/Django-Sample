'use strict';

define(['app'], function(app) {

	app.register.controller('forgot-passwordCtrl', ["$resource","$scope", "rest", 
		function($resource, $scope) {
    		var AuthForgot =  $resource("http://:url/accounts/forgot-password", {
                url: $scope.restURL
            });

    		$scope.user = {
				email: '',
			}
	
			$scope.submit = function() {
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();
				$scope.authToken = AuthForgot.save($scope.user, function() {
					window.location = "/";
				},function(error) {
					$scope.message = error.data;
				});
			}

    }]);


});