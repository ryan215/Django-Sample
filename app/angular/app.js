/*######################################################
 This app returns a ng module which is declared to
 be the main module for the entire app.

 Logic can be applied to set up the home page
 ######################################################*/
'use strict';
define(['angularAMD',
        'uiRouter',
        'geolocation',
        'uiBootstrap',
        'routeResolver',
        'angularResource',
        'angularLocalStorage',
        'autoFillEvent',
        'jquery',
        'jqueryui',
        'fullcalendar',
        'ui.calendar',
        'ui.utils',
        'ngTagsInput',
        'underscore',
        'angular-google-maps',
        'stripeJS',
        'stripe',
        "xeditable",
        'jcrop',
        'angularFileUpload',
        'bootstrap.wysihtml5.en-US',
        'socialShare',
        'mention',
        'caret',
        'angular-animate',
        'toasterjs',
        'bootstrap-typeahead',
        'mm.foundation',
        'angular-sanitize',
        'angular-social',
        'infinite-scroll'
    ],
    function (angularAMD) {
        'use strict';
        var app = angular.module('app', [
            'ui.router',
            'ui.route',
            'ui.bootstrap',
            'ui.bootstrap.datepicker',
            'ngTagsInput',
            'ui.bootstrap.timepicker',
            'ui.bootstrap.modal',
            'ui.bootstrap.carousel',
            'routeResolverServices',
            'ngResource',
            'LocalStorageModule',
            'ui.calendar',
            'ui.bootstrap.tabs',
            'ui.bootstrap.pagination',
            'google-maps',
            'xeditable',
            'toaster',
            'geolocation',
            'angularFileUpload',
            'td.easySocialShare',
            'mm.foundation',
            'ngSanitize',
            'ngSocial',
            'infinite-scroll'
        ]);

        app.run(function ($rootScope, $http, $tour, localStorageService, editableOptions, $resource) {
            $rootScope.toggleDashboard = function () {
                $rootScope.dashCollapsed = !$rootScope.dashCollapsed;
            };
            $rootScope.startTour = function () {
                $rootScope.fanaticsCollapsed = true;
                $rootScope.dashCollapsed = false;
                if ($rootScope.tourFinished == false) {
                    $tour.start();
                }
            };
            $tour.finished = function () {
                $rootScope.fanaticsCollapsed = false;
                $rootScope.dashCollapsed = true;
                $rootScope.tourFinished = localStorageService.set(true);
            };
            $rootScope.startTour();
            $rootScope.dashCollapsed = true;
            $rootScope.serverProtocal = "https";
            $rootScope.fanaticsCollapsed = false;
            $rootScope.serverURL = "app.liveeverfit.com";
            editableOptions.theme = 'bs3';
            $rootScope.token = localStorageService.get('Authorization');
            $rootScope.user_type = localStorageService.get('user_type');
            $http.defaults.headers.common['Authorization'] = localStorageService.get('Authorization');

            var mentionCollection = $resource("https://:url/feed/typeahead", {
                url: 'api.liveeverfit.com'
            });
            mentionCollection.get(function (mentions) {
                $rootScope.mentions = mentions.results;
            });
            if(navigator.splashscreen) {
                setTimeout(function() {
                    navigator.splashscreen.hide();
                }, 1000);
            }
        });

        app.config(['routeResolverProvider', '$stateProvider', '$urlRouterProvider', '$httpProvider',
            function (routeResolverProvider, $stateProvider, $urlRouterProvider, $httpProvider) {
                var route = routeResolverProvider.route;
                $stateProvider
                    //LoggedIn and LoggedOut
                    .state('home', route.resolve('/', 'home'))
                    .state('home.entry', route.resolve('entry/:id', 'home'))
                    .state('footer', route.resolve('/', 'footer'))

                    //LoggedOut
                    .state('about', route.resolve('/about', 'about'))
                    .state('contact', route.resolve('/contact', 'contact'))
                    .state('forgot-password', route.resolve('/forgot-password', 'auth/forgot-password'))
                    .state('reset-password', route.resolve('/reset-password/:change_password_token/:email', 'auth/reset-password'))
                    .state('registration', route.resolve('/registration', 'auth/registration'))
                    .state('registration.tier', route.resolve('/:tier', 'auth/registration'))
                    .state('registration.tier.profession', route.resolve('/:pro', 'auth/registration'))
                    .state('login', route.resolve('/login', 'auth/login'))

                    //LoggedIN
                    .state('settings', route.resolve('/settings', 'settings'))
                    .state('messages', route.resolve('/messages', 'messages'))
                    .state('messages.view', route.resolve('/:view', 'messages'))
                    .state('messages.view.reply', route.resolve('/reply/:recipient', 'messages'))
                    .state('messages.view.detail', route.resolve('/:index', 'messages'))
                    .state('workouts', route.resolve('/workouts', 'workouts'))
                    .state('workouts.video', route.resolve('/:id', 'workouts'))
                    .state('groups', route.resolve('/groups/:group', 'groups'))
                    .state('fitness-professionals', route.resolve('/fitness-professionals', 'fitness-professionals'))
                    .state('evergreen', route.resolve('/evergreen', 'evergreen'))
                    .state('change-password', route.resolve('/change-password', 'auth/change-password'))
                    .state('terms', route.resolve('/terms', 'terms'))
                    .state('verbiage', route.resolve('/verbiage', 'verbiage'))
                    .state('clients', route.resolve('/clients', 'clients'))
                    .state('faq', route.resolve('/faq', 'faq'))
                    .state('membership', route.resolve('/membership', 'membership'))
                    .state('membership.tier', route.resolve('/:tier', 'membership'))
                    .state('membership.tier.profession', route.resolve('/:pro', 'membership'))
                    .state('calendar', route.resolve('/calendar', 'calendar'))
                    .state('profile', route.resolve('/profile', 'profile'))
                    .state('profile.view', route.resolve('/:view', 'profile'))
                    .state('entry', route.resolve('/entry/:entry', 'profile'))
                    .state('greentree', route.resolve('/greentree', 'greentree'))
                    .state('marketing-materials', route.resolve('/marketing-materials', 'marketing-materials'))
                    .state('streaming-classes', route.resolve('/streaming-classes', 'streaming-classes'))
                    .state('upgrade', route.resolve('/upgrade', 'upgrade'))
                    .state('shop', route.resolve('/shop', 'shop'))
                    .state('shop.greentree', route.resolve('/greentree', 'shop'))
                    .state('shop.cart', route.resolve('/cart', 'shop'))
                    .state('shop.returns', route.resolve('/returns', 'shop'))
                    .state('shop.streaming-classes', route.resolve('/streaming-classes', 'shop'))
                    .state('shop.collection', route.resolve('/:collection', 'shop'))
                    .state('shop.collection.type', route.resolve('/:type', 'shop'))



                    .state('test', route.resolve('/test', 'test'))
                    .state('test.redirect', route.resolve('/:redirect', 'test'));

                $urlRouterProvider.otherwise("/");

                $httpProvider.interceptors.push('httpInterceptor');
            }
        ]);


        app.service('rest', ['$rootScope', function ($rootScope) {
            $rootScope.restProtocol = "https";
            $rootScope.restURL = "api.liveeverfit.com";
        }]);
        app.service('restricted', ['$rootScope', 'localStorageService', '$http', function ($rootScope, localStorageService, $http) {
            $rootScope.restricted = function () {
                $rootScope.token = localStorageService.get('Authorization');
                $rootScope.user_type = localStorageService.get('user_type');
                $http.defaults.headers.common['Authorization'] = localStorageService.get('Authorization');
                setTimeout(function () {
                    if ($rootScope.token === null) {
                        window.location = "#/login";
                    }
                });
            };
        }]);

        app.service('tokenError', ['localStorageService', '$rootScope', function (localStorageService, $rootScope) {
            $rootScope.checkTokenError = function (error) {
                if (error.data && error.data['detail'] == 'Invalid token') {
                    localStorageService.clearAll();
                    $rootScope.restricted();
                }
            }
        }]);

        app.controller('NavCtrl', ['$rootScope', 'localStorageService', '$resource', '$state', '$timeout', '$scope', 'toaster', 'rest', 'restricted',
            function ($rootScope, localStorageService, $resource, $state, $timeout, $scope, toaster) {

                $scope.isCollapsed = true;
                var notificationsResource = $resource(":protocol://:url/notifications/", {
                    protocol: $scope.restProtocol,
                    url: $scope.restURL
                }, {update: { method: 'PUT' }});
                var notificationsIdResource = $resource(":protocol://:url/notifications/:id", {
                    id: '@id',
                    protocol: $scope.restProtocol,
                    url: $scope.restURL
                }, {update: { method: 'PUT' }});
                var tagsResource = $resource(":protocol://:url/tags/", {
                    protocol: $scope.restProtocol,
                    url: $scope.restURL
                }, {update: { method: 'PUT' }});


                $scope.tagsCall = tagsResource.get($scope.user, function () {
                    $scope.temTags = $scope.tagsCall.results;
                }, function (error) {
                    $scope.message = error.data;
                });

                $scope.tick = function () {
                    if ($rootScope.token !== null) {
                        $scope.notifications = notificationsResource.get(function () {
                            $scope.notificationsCount = $scope.notifications.count;
                            $timeout($scope.tick, 30000);
                        });
                    }
                    else {
                        $timeout($scope.tick, 30000);
                    }
                };
                $scope.tick();

                $scope.signOut = function () {
                    localStorageService.clearAll();
                    $scope.restricted();
                };

                $scope.pop = function () {
                    angular.forEach($scope.notifications.results, function (value, key) {
                        toaster.pop(value.level, value.level, value.message, value.target_content_type, value.target_object_id);
                    });
                };

                $scope.clickToasterContainer = function (toaster) {
                    angular.forEach($scope.notifications.results, function (value, key) {
                        if (toaster.notificationId == value.target_object_id){

                            if(toaster.notificationType == 'entry'){
                                $state.go('entry', {entry: value.target_object_id}, { reload: true});
                            }
                            else if(toaster.notificationType == 'Message'){
                                $state.go('messages', {}, { reload: true});
                            }
                            else if(toaster.notificationType == 'user'){
                                $state.go('profile', {}, { reload: true});
                            }
                            var notificationsCallback = notificationsIdResource.update({id: value.id}, function () {
                                $rootScope.$$childHead.tick();
                            });
                        }
                    });
                };


            }]);

        app.controller('footerCtrl', ['localStorageService', '$scope',
            function (localStorageService, $scope) {
                $scope.isCollapsed = true;
                $scope.templateNav = {
                    url: 'footer/index.html'
                };
            }]);
        app.controller('fanaticsCtrl', ['localStorageService', '$scope', '$resource', '$q', '$state',
            function (localStorageService, $scope, $resource, $q, $state) {
                angular.extend($scope, {
                    fanaticSearch: '',
                    fanaticList: [],
                    fanaticCollection: $resource(":protocol://:url/users/fanatics", {
                        protocol: $scope.restProtocol,
                        url: $scope.restURL
                    }, {'query': {method: 'GET', isArray: false }}),
                    fitFriendsCollection: $resource(":protocol://:url/users", {
                        protocol: $scope.restProtocol,
                        url: $scope.restURL
                    }, {'query': {method: 'GET', isArray: false }}),
                    fanaticTypeahead: function (query) {
                        var deferred = $q.defer();
                        $scope.fitFriendsCollection.query({
                            search: query
                        }, function (data) {
                            deferred.resolve(data.results);
                        });
                        return deferred.promise;
                    },
                    onSelect: function ($item) {
                        $state.go('profile.view', {view: $item.id})
                    }
                });
                $scope.fanaticCollection.get({}, function (data) {
                    $scope.fanaticList = data.results;
                });
            }]);
        app.directive('ng-blur', function () {
            return {
                restrict: 'A',
                link: function postLink(scope, element, attrs) {
                    element.bind('blur', function () {
                        scope.$apply(attrs.ngBlur);
                    });
                }
            };
        });
        app.directive('ngEnter', function () {
            return function (scope, element, attrs) {
                element.bind("keydown keypress", function (event) {
                    if (event.which === 13) {
                        scope.$apply(function () {
                            scope.$eval(attrs.ngEnter);
                        });
                        event.preventDefault();
                    }
                });
            };
        });
        app.directive('tagSpecialties', function () {
            return {
                restrict: "A",
                require: '?ngModel',
                link: function (scope, element, attrs, ngModel) {
                    if (!ngModel) return; // do nothing if no ng-model
                    ngModel.$render = function () {
                        var $dropdown = $('<div class="dropdown"></div>'),
                            $toggle = $('<div class="tag tag-blue tag-click">more <i class="fa fa-chevron-right"></i></div>'),
                            $element = $(element).empty().append($dropdown).append($toggle),
                            width = $element.width(),
                            tagsWidth = $toggle.width() + 12;
                        $toggle.hide();
                        $toggle.click(function() {
                            $dropdown.toggle();
                            if($dropdown.css('display') == 'none') $toggle.html('more <i class="fa fa-chevron-right"></i>');
                            else $toggle.html('<i class="fa fa-chevron-left"></i> less');
                        });
                        angular.forEach(ngModel.$viewValue, function(value, index) {
                            var $tag = $('<span class="tag tag-blue tag-click">' + value + '</span>'),
                                tagWidth = 0;
                            $tag.insertBefore($toggle);
                            tagWidth = $tag.width() + 20;
                            tagsWidth += tagWidth;
                            if(tagsWidth > width) {
                                $toggle.show();
                                tagsWidth -= tagWidth;
                                $tag.remove();
                                $dropdown.append($tag);
                            }
                        });
                    };
                    $(window).resize(_.debounce(ngModel.$render, 350));
                }
            };
        });
        app.directive('richTextEditor', function () {
            return {
                restrict: "A",
                require: '?ngModel',
                replace: true,
                transclude: true,
                template: '<div><textarea></textarea></div>',
                link: function (scope, element, attrs, ngModel) {
                    if (!ngModel) return; // do nothing if no ng-model
                    var textarea = $(element.find('textarea')).wysihtml5(),
                        editor = textarea.data('wysihtml5').editor;
                    // view -> model
                    editor.on('change', function () {
                        if (editor.getValue())
                            scope.$apply(function () {
                                ngModel.$setViewValue(editor.getValue());
                            });
                    });
                    // model -> view
                    ngModel.$render = function () {
                        textarea.html(ngModel.$viewValue);
                        editor.setValue(ngModel.$viewValue);
                    };
                    ngModel.$render();
                }
            };
        });
        app.directive('ngInput', [function () {
            return {
                restrict: 'A', // only activate on element attribute
                require: '?ngModel', // get a hold of NgModelController
                link: function (scope, element, attrs, ngModel) {
                    if (!ngModel) return; // do nothing if no ng-model
                    var initMentions = function() {
                        if (scope.mentions) {
                        // Feed Typeahead
                            element.mention({
                                delimiter: '@',
                                queryBy: ['name'],
                                emptyQuery: true,
                                users: scope.mentions,
                                typeaheadOpts: {
                                    items: 8 // Max number of items you want to show
                                }
                            });
                        }
                        else {
                            setTimeout(initMentions, 400);
                        }
                    };
                    initMentions();


                    // Specify how UI should be updated
                    ngModel.$render = function () {
                        element.html(ngModel.$viewValue || '');
                    };

                    // Listen for change events to enable binding
                    element.on('blur keyup change', function (e) {
                        scope.$apply(readViewText);
                    });

                    // Write data to the model
                    function readViewText() {
                        //var html = element.val();
                        // Top line works for input and text area
                        var html = element.html();
                        // When we clear the content editable the browser leaves a <br> behind
                        // If strip-br attribute is provided then we strip this out
                        if (attrs.stripBr && html == '<br>') {
                            html = '';
                        }
                        ngModel.$setViewValue(html);
                    }
                }
            };
        }]);
        app.factory('fileReader', function ($q) {
            var onLoad = function (reader, deferred, scope) {
                return function () {
                    scope.$apply(function () {
                        deferred.resolve(reader.result);
                    });
                };
            };
            var onError = function (reader, deferred, scope) {
                return function () {
                    scope.$apply(function () {
                        deferred.reject(reader.result);
                    });
                };
            };
            var onProgress = function (reader, scope) {
                return function (event) {
                    scope.$apply(function () {
                        scope.percent = parseInt(100.0 * event.loaded / event.total);
                    });
                };
            };
            var getReader = function (deferred, scope) {
                var reader = new FileReader();
                reader.onload = onLoad(reader, deferred, scope);
                reader.onerror = onError(reader, deferred, scope);
                reader.onprogress = onProgress(reader, scope);
                return reader;
            };
            var readAsDataURL = function (file, scope) {
                var deferred = $q.defer();
                var reader = getReader(deferred, scope);
                reader.readAsDataURL(file);
                return deferred.promise;
            };
            return { readAsDataUrl: readAsDataURL };
        });
        app.directive('disableNgAnimate', ['$animate', function ($animate) {
            return {
                restrict: 'A',
                link: function (scope, element) {
                    $animate.enabled(false, element);
                }
            };
        }]);
        app.factory('httpInterceptor', function ($q, $rootScope, $log) {
            /*
             Http interceptor for when making an API request, allows
             easy integration with the "loader" directive to add the spinner
             anywhere easily.
             */
            var numLoadings = 0;
            return {
                request: function (config) {
                    numLoadings++;
                    // Show loader
                    $rootScope.$broadcast("loader_show");
                    return config || $q.when(config)

                },
                response: function (response) {
                    if ((--numLoadings) === 0) {
                        // Hide loader
                        $rootScope.$broadcast("loader_hide");
                    }
                    return response || $q.when(response);

                },
                responseError: function (response) {
                    if (!(--numLoadings)) {
                        // Hide loader
                        $rootScope.$broadcast("loader_hide");
                    }
                    return $q.reject(response);
                }
            };
        });
        app.directive("loader", function ($rootScope) {
            return function ($scope, element, attrs) {
                // on first load, hides all spinners until
                // the broadcast calls them
                $scope.$on("loader_show", function () {
                    return element.addClass('show');
                });
                $scope.$on("loader_hide", function () {
                    return element.removeClass('show');
                });
            };
        });
        app.directive('clickOnce', function ($timeout) {
            return {
                restrict: 'A',
                link: function (scope, element, attrs) {
                    var replacementText = attrs.clickOnce;

                    element.bind('click', function () {
                        $timeout(function () {
                            if (replacementText) {
                                element.html(replacementText);
                            }
                            element.attr('disabled', true);
                        }, 0);
                    });
                }
            };
        });
        //Bootstrap Angular
        angularAMD.bootstrap(app);
        return app;
    });
