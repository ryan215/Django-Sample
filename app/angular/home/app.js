'use strict';
define(['app', 'feed'], function (app) {
    app.register.controller('homeCtrl', ['$scope', 'restricted',
        function ($scope) {
            $scope.restricted();
        }]);
    app.register.controller('homeController', ['localStorageService', '$scope', '$resource', '$state', '$stateParams', 'promiseService', 'restricted',
        function (localStorageService, $scope, $resource, $state, $stateParams) {
            angular.extend($scope, {
                tabs: [
                    {title: 'all', filter: '', active: true},
                    {title: 'statuses', filter: 'text'},
                    {title: 'photos', filter: 'photo'},
                    {title: 'videos', filter: 'video'},
                    {title: 'blogs', filter: 'blog'},
                    {title: 'events', filter: 'event'}
                ],
                initFeed: function() {
                    $scope.feed = {
                        filter: $stateParams.id ? '/entry/' + $stateParams.id : undefined,
                        show: true
                    };
                },
                feed: {
                    filter: undefined,
                    show: false
                },
                feedFilter: function (type) {
                    $scope.feed = {
                        filter: type ? '/' + type : ''
                    };
                }
            });
            $scope.$on('$stateChangeSuccess', $scope.initFeed);
            $scope.initFeed();

            $scope.onSelect = function($item, $model, $label){
                $state.go('profile.view', {view: $item.id})
            }
            

        }]);
    app.register.controller('BannerCtrl', ['$scope',
        function ($scope) {
            var slides = $scope.slides = [
                {
                    image: 'home/img/slider/1.png'
                },
                {
                    image: 'home/img/slider/3.png',
                    url: 'http://store.liveeverfit.com/'
                },
                {
                    image: 'home/img/slider/4.png',
                    url: 'http://store.liveeverfit.com/pages/greentree-foods'
                },
                {
                    image: 'home/img/slider/5.png',
                    url: 'http://store.liveeverfit.com/collections/trx'
                },
                {
                    image: 'home/img/slider/7.png'
                }
            ];
        }]);
    app.register.service('promiseService', function ($q, $rootScope) {
        $rootScope.q = $q
    });
    return app;
});