'use strict';

define(['app'], function(app) {
    app.register.controller('footerCtrl', ['localStorageService','$scope', 
    	function(localStorageService,$scope) {
    		$scope.token = localStorageService.get('Authorization');
            if ($scope.token === null) {
              $scope.homeTemplate = {name: 'loggedout.html', url: 'home/loggedout.html'};
            } else {
              $scope.homeTemplate = {name: 'loggedin.html', url: 'home/loggedin.html'};
            }
    }]);
    return app;
});