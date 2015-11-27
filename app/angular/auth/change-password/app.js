'use strict';

define(['app'], function(app) {

	app.register.controller('change-passwordCtrl', ['$scope', 'restricted', 
    	function($scope) {
            $scope.restricted();
    }]);


    app.register.controller('changeCtrl', ["localStorageService","$resource","$scope", "rest",
    	function(localStorageService, $resource, $scope) {
    		var AuthChange =  $resource("http://:url/accounts/change-password", {
                url: $scope.restURL
            });

    		$scope.user = {
				token: localStorageService.get('rest_token'),
				current_password: '',
				password: '',
				password2: '',
			}
	
			$scope.submit = function() {
                // AutoFill Fix
                angular.element(document.getElementsByTagName('input')).checkAndTriggerAutoFillEvent();
				$scope.authToken = AuthChange.save($scope.user, function() {
					window.location = "/#/logout";
				},function(error) {
					$scope.message = error.data;
				});
			}
	
	}]);


});