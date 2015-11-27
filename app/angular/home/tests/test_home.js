'use strict'

define(['app', 'angularAMD', '/base/test_app.js'], function (app, angularAMD) {
    'use strict';
    describe("Home Test:", function () {
        //define variables to use in this scope
        var route, path, scope, ctrl;

        /// This down here isn't really doing what I want it to do....
        it('should be loaded with routerResolver', function () {
            angularAMD.inject(function ($rootScope, routeResolver) {
                scope = $rootScope.$new();
                route = routeResolver.route;
            });
            path = route.resolve('/', 'home');
            expect(path.templateUrl).toBe('home/index.html');
            expect(path.controller).toBe('homeCtrl');
            expect(path.url).toBe('/');
        });

        require(['/base/home/app.js'], function() {
            it('should be registered to app', function () {
                angularAMD.inject(function ($controller) {
                    ctrl = $controller('homeCtrl', { $scope: scope });
                });
                expect(ctrl).toBeDefined();
            });

            it('should set a homeTemplate', function () {
                angularAMD.inject(function ($controller) {
                    ctrl = $controller('homeCtrl', { $scope: scope });
                });
                expect(scope.homeTemplate).toBeDefined();
            });
        });
    });
});