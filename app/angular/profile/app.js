'use strict';
define(['app', 'feed', 'calendar'], function (app) {
    app.register.controller('profileCtrl', ['$scope', '$modal', 'rest', 'restricted',
        function ($scope) {
            $scope.restricted();
        }]);
    app.register.controller('photoChangeCtrl', ['$scope', '$resource', '$modalInstance', '$upload', 'localStorageService', 'fileReader',
        function ($scope, $resource, $modalInstance, $upload, localStorageService, fileReader) {
            $scope.user_id = localStorageService.get('user_id');
            $scope.message = {};
            $scope.closeAlert = function (error) {
                delete $scope.message[error];
            };
            $scope.onFileSelect = function ($files) {
                $scope.uploadImg = $files[0];
                $scope.upload = $upload.upload({
                    url: $scope.restProtocol + '://' + $scope.restURL + '/upload-image/upload-profile-picture',
                    file: $scope.uploadImg
                }).progress(function (evt) {
                    $scope.percent = parseInt(100.0 * evt.loaded / evt.total);
                }).success(function (data) {
                    fileReader.readAsDataUrl($scope.uploadImg, $scope).then(function (result) {
                        $scope.imgSrc = result;
                        $scope.percent = undefined;
                    });
                    delete $scope.uploadImg;
                    $scope.returnData = data;
                }).error(function (data) {
                    $scope.percent = false;
                    angular.extend($scope.message, data);
                });
            };
            $scope.ok = function () {
                if($scope.cords) {
                    var cords = $scope.cords,
                        widthHeight = $scope.widthHeight;
                    $scope.upload = $upload.upload({
                        url: $scope.restProtocol + '://' + $scope.restURL + '/upload-image/crop-profile-picture',
                        data: {
                            id: $scope.returnData.id,
                            cropping: cords.x + ',' + cords.y + ',' + cords.x2 + ',' + cords.y2,
                            WidthHeight: widthHeight.w + ',' + widthHeight.h,
                            user_id: $scope.user_id
                        }
                    }).progress(function (evt) {
                        $scope.percent = parseInt(100.0 * evt.loaded / evt.total);
                    }).success(function (data) {
                        $modalInstance.close(data);
                    }).error(function (data) {
                        $scope.percent = undefined;
                        angular.extend($scope.message, data);
                    });
                }
                else {
                    angular.extend($scope.message, {
                        "image": ["Image not cropped."]
                    });
                }
            };
            $scope.cancel = function () {
                $modalInstance.dismiss();
            };
        }]);
app.register.directive('cropImg', ['$window',
        function ($window, shareImg) {
            return {
                restrict: 'E',
                replace: true,
                scope: {
                    src: '='
                },
                link: function (scope, element) {
                    var clear = function () {
                        if (element.myImg) {
                            element.myImg.remove();
                            delete element.myImg;
                        }
                    };
                    scope.$on('$destroy', clear);
                    scope.$watch('src', function (src) {
                        clear();
                        if (!src) return;
                        element.after('<img style="display: none;"/>');
                        element.myImg = element.next();
                        element.myImg.attr('src', src);
                        element.myImg.on('load', function () {
                            var width = this.width,
                                height = this.height;
                            element.myImg.addClass('crop-img').show()
                            .Jcrop({
                                minSize: [500, 500],
                                trueSize: [width, height],
                                onSelect: function (cords) {
                                    scope.$parent.$parent.$apply(function () {
                                        scope.$parent.$parent.cords = cords;
                                        scope.$parent.$parent.widthHeight = {
                                            w: width,
                                            h: height
                                        };
                                    });
                                },
                                setSelect: [0,0,500,500],
                                aspectRatio: 1
                            });
                        })
                    });
                }
            };
        }]);

    app.register.controller('profileController', ['$scope', "$state", "$stateParams", '$resource', '$modal', '$http', '$location', '$window', 'localStorageService', 'rest', 'tokenError',
        function ($scope, $state, $stateParams, $resource, $modal, $http, $location, $window, localStorageService, tokenError) {
            angular.extend($scope, {
                calendarShow: false,
                user_id: localStorageService.get('user_id'),
                user_type: localStorageService.get('user_type'),
                entry : '',
                feed: {
                    id: undefined,
                    filter: undefined,
                    show: false
                },
                feedActive: true,
                filter: function (type) {
                    if (type == 'exempt') {
                        angular.extend($scope.feed, {
                            show: false
                        });
                    }
                    // IDK if this is neaded or if we can filter it in the backend by type...
//                    else if (type == 'transformation') {
//                        $scope.feed = {
//                            id: $scope.profile_user.id,
//                            filter: '/group/transformation',
//                            show: true
//                        };
//                    }
                    else {
                        $scope.feed = {
                            id: $scope.profile_user.id,
                            filter: type?'/'+type+'/list':'',
                            show: true
                        };
                    }
                },
                clientFilter: function() {
                    $scope.feed = {
                        id: $stateParams.view == $scope.user_id ? null : $stateParams.view,
                        filter: '/client',
                        show: true
                    };
                },
                userResource: $resource(":protocol://:url/users/profile/:id/", {
                    protocol: $scope.restProtocol,
                    url: $scope.restURL,
                    id: "@id"
                }, {update: { method: 'PUT' }}),
                entryResource : $resource(":protocol://:url/feed/entry/:id/", {
                    protocol: $scope.restProtocol,
                    url: $scope.restURL,
                    id: "@id"
                }, {update: { method: 'PUT' }}),
                followResource: $resource(":protocol://:url/users/follow/:id/", {
                    protocol: $scope.restProtocol,
                    url: $scope.restURL,
                    id: "@id"
                }, {update: { method: 'PUT' }}),
                blockResource: $resource(":protocol://:url/users/block/:id/", {
                    protocol: $scope.restProtocol,
                    url: $scope.restURL,
                    id: "@id"
                }, {update: { method: 'PUT' }}),
                connectResource: $resource(":protocol://:url/users/connect/:id/", {
                    protocol: $scope.restProtocol,
                    url: $scope.restURL,
                    id: "@id"
                }, {update: { method: 'PUT' }}),
                followToggle: function () {
                    $scope.followResource.update({id: $scope.user_id, user_id: $scope.profile_user.id}, function (data) {

                        $scope.profile_user.user_follows = data.user_follows;
                    });
                },
                blockToggle: function () {
                    $scope.blockResource.update({id: $scope.user_id, user_id: $scope.profile_user.id}, function (data) {

                        $scope.profile_user.user_blocks = data.user_blocks;
                    });
                },
                connect: function () {
                    if($scope.user_type == 'user'){
                        localStorageService.add('profesional', $scope.profile_user.id);
                        $state.go('upgrade');
                    }else{
                        $scope.connectResource.update({id: $scope.user_id, professional_id: $scope.profile_user.id}, function (data) {
                            $scope.profile_user.user_connected = data.user_connected
                        });
                    }
                },
                getProfile: function () {
                    $scope.userResource.get({id: $stateParams.view || $scope.user_id}, function (data) {
                        $scope.feedActive = true;
                        $scope.profile_user = data;
                        $scope.feed = {
                            id: $scope.profile_user.id,
                            filter: $scope.feed.filter,
                            show: $scope.feed.show
                        };
                        // Add Click functions to Map Referrals
                        angular.forEach($scope.profile_user.referrals, function (value, key) {
                            angular.extend($scope.profile_user.referrals[key], {
                                click: function () {
                                    $state.go('profile.view', {view: $scope.profile_user.referrals[key].id});
                                }
                            });
                        });

                    }, $scope.checkTokenError);
                },
                referralIcon: {
                    //url: encodeURI('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" width="30px" height="50px" viewBox="0 0 30 50" ><path fill="#1A8CFF" d="M8.018,13.542c0.05-2.435,2.312-4.583,4.752-4.47c2.333,0.001,4.469,2.031,4.556,4.369 c0.032,1.122,0.006,2.245,0.014,3.367c0.76,0.067,1.5,0.296,2.159,0.678c1.281-0.157,2.648,0.076,3.714,0.831 c0.167,0.109,0.338,0.246,0.552,0.22c1.252,0.002,2.538,0.396,3.473,1.252c0.97,0.861,1.541,2.11,1.696,3.388 c0.192,1.532-0.075,3.078-0.454,4.561c-0.494,1.937-1.371,3.761-1.74,5.73c-0.1,0.506-0.063,1.022-0.069,1.533 c0,1.399-0.002,2.799,0,4.199c0.004,0.491-0.08,1-0.357,1.417c-0.417,0.672-1.183,1.101-1.973,1.099 c-3.639,0.012-7.277,0.004-10.914,0.005c-0.492-0.005-0.998,0.033-1.473-0.121c-0.931-0.296-1.617-1.222-1.607-2.204 c-0.006-1.558,0-3.114-0.003-4.672c-0.003-0.384,0.052-0.801-0.161-1.144c-0.56-0.883-1.372-1.564-2.167-2.226 c-0.757-0.649-1.535-1.285-2.391-1.802c-1.195-0.658-2.497-1.157-3.554-2.04c-0.573-0.479-1.006-1.163-1.045-1.922 c-0.048-1.283,0.241-2.612,0.995-3.67c0.549-0.804,1.397-1.398,2.348-1.619c1.204-0.284,2.482-0.158,3.644,0.246 C8.016,18.211,8.001,15.876,8.018,13.542z M10.346,13.729c-0.006,3.502,0,7.004-0.003,10.507 c-0.614-0.067-1.136-0.423-1.651-0.737c-0.71-0.473-1.507-0.826-2.352-0.967c-0.714-0.091-1.523-0.086-2.104,0.4 c-0.669,0.582-0.871,1.521-0.888,2.373c-0.025,0.25,0.208,0.406,0.379,0.543c0.538,0.385,1.133,0.681,1.722,0.979 c1.658,0.765,3.116,1.888,4.464,3.106c0.862,0.788,1.811,1.54,2.344,2.605c0.371,0.663,0.442,1.439,0.417,2.187 c3.888-0.002,7.773,0,11.662-0.002c-0.055-1.26,0.201-2.508,0.605-3.694c0.396-1.194,0.798-2.387,1.181-3.587 c0.407-1.321,0.671-2.725,0.469-4.107c-0.115-0.761-0.447-1.535-1.102-1.98c-0.829-0.562-1.893-0.545-2.846-0.424 c-0.208-0.192-0.351-0.458-0.597-0.612c-0.861-0.588-2.065-0.76-2.998-0.233c-0.3-0.279-0.617-0.549-0.996-0.712 c-0.984-0.446-2.184-0.245-3.045,0.38c-0.008-2.01,0.004-4.02-0.004-6.03c0.019-1.168-0.981-2.238-2.143-2.316 C11.572,11.281,10.339,12.441,10.346,13.729z M22.793,37.118c-0.51,0.172-0.865,0.722-0.772,1.26 c0.069,0.612,0.692,1.099,1.306,0.997c0.646-0.074,1.137-0.758,0.986-1.393C24.188,37.321,23.426,36.873,22.793,37.118z"/></svg>')
                    url: encodeURI('data:image/svg+xml;charset=utf-8,<svg width="38" height="38" xmlns="https://www.w3.org/2000/svg"><path fill="rgb(26, 140, 255)" d="m22.18,35.598c-2.943001,0.304001 -5.249001,-1.25 -6.413,-3.172001c-1.439,-2.379999 -3.078,-4.518999 -4.6,-6.806999c-0.960999,-1.438 -1.921,-2.924999 -3.043,-4.529999c-0.406,-0.581001 -0.99,-1.385 -1.684,-2.136002c-0.537,-0.577 -1.564,-1.595999 -1.427,-2.203999c0.346,-1.539001 4.026,-0.458 4.729,0c0.356,0.233 0.64,0.682999 0.975,1.035999c0.92,0.98 1.925,2.07 2.847,3.044001c-0.115,-3.870001 -0.065001,-9.158001 -0.065001,-13.73c0,-1.96 -0.344999,-4.596 1.491,-4.73c0.994,-0.074 1.937,0.656 2.204,1.425c0.285999,0.814 0.128,2.03 0.128,3.109c0,3.085 0.337,6.325 0.26,9.261c1.984999,0.247 4.417999,0.492001 6.543999,0.712c0.771,0.083 1.575001,0.041 2.202,0.197001c1.194,0.292999 2.612001,0.967001 2.654001,2.006001c0.136,3.383999 -0.469,7.202 -0.868,10.563999c-0.201,1.679001 -1.052999,3.004999 -2.045,4.009001c-0.958,0.970001 -2.289,1.780998 -3.889,1.945999z"/></svg>')
                },
                initReach: function () {
                    $scope.hideFeed();
                    $scope.map.control.refresh({
                        latitude: 38.828127,
                        longitude: -98.579404
                    });
                },
                initCalendar: function () {
                    $scope.showCalendar = true;
                    $scope.hideFeed();
                },
                map: {
                    center: {
                        latitude: 39.828127,
                        longitude: -98.579404
                    },
                    zoom: 4,
                    control: {
                    },
                    options: {
                        zoomControlOptions: {
                            style: google.maps.ZoomControlStyle.SMALL
                        }
                    }
                },
                hideFeed: function () {
                    angular.extend($scope.feed, {
                        show: false
                    });
                },
                photoChange: function () {
                    var modalInstance = $modal.open({
                        templateUrl: '../settings/modals/photoChange.html',
                        controller: 'photoChangeCtrl'
                    });
                    modalInstance.result.then(function (data) {
                        data.path = data.path.substring(6);
                        $scope.profile_user.img = data.path;
                        localStorageService.add('user_img',"/media" + $scope.profile_user.img);
                    }, $.noop());
                },
                entryAffiliate: function (where) {
                                var i,
                                theLink,
                                pageLink = encodeURIComponent($location.absUrl()+ "profile/" + $scope.user_id + '?referral=' + $scope.user_email),
                                pageTitleUri = encodeURIComponent('Check my page out on Liveeverfit! '),
                                shareLinks = [];
                                switch (where) {
                                    case 'twitter':
                                      theLink = 'https://twitter.com/intent/tweet?text=' + pageTitleUri + '%20' + pageLink;
                                      break;
                                    case 'facebook':
                                      theLink = 'https://facebook.com/sharer.php?u=' + pageLink;
                                      break;
                                    case 'linkedin':
                                      theLink = 'https://www.linkedin.com/shareArticle?mini=true&url=' + pageLink + '&title=' + pageTitleUri;
                                      break;
                                }
                                $window.open(theLink);

                            },

            });
            //init view
            $scope.$on('$stateChangeSuccess', $scope.getProfile);
        }
    ]);
});