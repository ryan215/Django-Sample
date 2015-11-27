'use strict';

define(['app', 'videojs'], function (app) {
    app.register.controller('messagesCtrl', ['$scope', 'restricted',
        function ($scope) {
            $scope.restricted();
        }]);


    app.register.controller('messagesController', ["$state", "$stateParams", "$sce", "$resource",
        "rest", "tokenError", "localStorageService", "$scope",
        "$anchorScroll", "promiseService", "$http", 
        function ($state, $stateParams, $sce, $resource, rest, tokenError, localStorageService, $scope) {
            $scope.user_id = localStorageService.get('user_id');
            $scope.user_type = localStorageService.get('user_type');
            $scope.selectedUser = null;
            $scope.inboxCollection = $resource(":protocol://:url/messages/inbox?page=:page", {
                page: $scope.currentPage,
                protocol: $scope.restProtocol,
                url: $scope.restURL
            });
            $scope.messageResource = $resource(":protocol://:url/messages/message/:id", {
                protocol: $scope.restProtocol,
                url: $scope.restURL,
                id: '@id'
            }, { 
                update: {
                    method: 'PUT'
                }
            });
            $scope.sentCollection = $resource(":protocol://:url/messages/sent?page=:page", {
                page: $scope.currentPage,
                protocol: $scope.restProtocol,
                url: $scope.restURL
            });
            $scope.trashCollection = $resource(":protocol://:url/messages/trash?page=:page", {
                page: $scope.currentPage,
                protocol: $scope.restProtocol,
                url: $scope.restURL
            });
            $scope.clientListCollection = $resource(":protocol://:url/users/professionals/client-list/", {
                protocol: $scope.restProtocol,
                url: $scope.restURL
            });
            $scope.newMessageResource = $resource(":protocol://:url/messages/compose/", {
                protocol: $scope.restProtocol,
                url: $scope.restURL
            });
            //
            $scope.connectionResource = $resource(":protocol://:url/messages/connection/:id", {
                protocol: $scope.restProtocol,
                url: $scope.restURL,
                id: '@id'
            }, { 
                update: {
                    method: 'PUT'
                }
            });
            $scope.replyMessageResource = $resource(":protocol://:url/messages/reply/:id", {
                id: '@id',
                protocol: $scope.restProtocol,
                url: $scope.restURL
            });
            $scope.deleteMessageResource = $resource(":protocol://:url/messages/delete/:id", {
                id: '@id',
                protocol: $scope.restProtocol,
                url: $scope.restURL
            }, { 
                update: {
                    method: 'PUT'
                }
            });
            $scope.submitMessage = function () {
                $scope.newMessage.recipient = $scope.selectedUser;
                $scope.newMessageResource.save($scope.newMessage, function () {
                    $state.go('messages.view', {view: 'inbox'});
                });
            };
            $scope.deleteMessage = function (index, msg) {
                var attrs;
                $scope.list.splice(index, 1);
                msg.view = $scope.view
                $scope.deleteMessageResource.update(msg, function(){

                });
                //$state.go('messages.view', {view: $scope.view});

            };
            $scope.$on('$stateChangeSuccess', function () {
                var successInbox = function (data) {
                        $scope.unread = 0;
                        $scope.list = data.results;
                        $scope.totalItems = data.count;
                        angular.forEach(data.results, function(value, key){
                            if(value.read_at == null){
                                $scope.unread = $scope.unread + 1
                            }
                        });
                        if ($stateParams.index) {
                            $scope.index = $stateParams.index;
                            $scope.detailIndex = $stateParams.index;
                            $scope.detail = $scope.list[$stateParams.index];
                        }
                    },
                    success = function (data) {
                        $scope.list = data.results;
                        $scope.totalItems = data.count;
                        if ($stateParams.index) {
                            $scope.index = $stateParams.index;
                            $scope.detailIndex = $stateParams.index;
                            $scope.detail = $scope.list[$stateParams.index];
                        }
                    },
                    views = {
                        inbox: function () {
                            $scope.inboxCollection.get({page:$scope.currentPage}, successInbox);
                        },
                        sent: function () {
                            $scope.sentCollection.get({page:$scope.currentPage}, success);
                        },
                        deleted: function () {
                            $scope.trashCollection.get({page:$scope.currentPage}, success);
                        },
                        new: function () {
                            

                            $scope.newMessage = {
                                body: '',
                                subject: '',
                                recipient: '',
                                input: ''
                                
                            };
                            $scope.connectionResource.update({id:$scope.user_id, user_id:$stateParams.recipient, subject:$stateParams.subject || null},function(data){
                                $scope.newMessage.type = data.user_type
                                console.log($scope.newMessage);
                                
                                if($scope.user_type == 'professional' && $stateParams.recipient){
                                    $scope.selectedUser = $stateParams.recipient
                                    $scope.newMessage.recipient = data.connection
                                    $scope.pro_connection = true;
                                }else if($scope.user_type == 'upgraded' && data.connection){
                                    $scope.newMessage.recipient = data.connection
                                    $scope.selectedUser = data.connection.id;
                                }
                                else{
                                    /*
                                    $scope.newMessage.recipient = null;
                                    $scope.selectedUser = null;
                                    $scope.pro_connection = false;
                                    */
                                    $scope.selectedUser = $stateParams.recipient
                                    $scope.newMessage.recipient = data.connection
                                    $scope.pro_connection = true;
                                }
                            });  
                        }
                    };
                if($stateParams.view) {
                    $scope.view =  $stateParams.view;
                    if ($stateParams.index != undefined && $scope.list) {
                        if($stateParams.view == 'inbox')
                        {
                            $scope.date = new Date();
                            $scope.messageResource.update({

                                id:$scope.list[$stateParams.index].id,
                                subject:$scope.list[$stateParams.index].subject,
                                read_at:$scope.date, 
                                body:$scope.list[$stateParams.index].body
                            },
                                
                                function(data){
                                
                                $scope.inboxCollection.get({page:$scope.currentPage}, function(data){
                                    $scope.unread = 0;
                                    angular.forEach(data.results, function(value, key){
                                        if(value.read_at == null){
                                            $scope.unread = $scope.unread + 1
                                        }
                                    });
                                });
                            });
                            $scope.list[$stateParams.index].read_at = $scope.date;

                        } 
                        $scope.detailIndex = $stateParams.index;
                        $scope.detail = $scope.list[$stateParams.index];
                    }
                    else {
                        $scope.detailIndex = -1;
                        $scope.detail = false;
                        //Run View Function
                        $scope.currentPage = 1;
                        views[$scope.view]();

                    }
                }
                else {
                    $state.go('messages.view', {view: 'inbox'});
                }
                $scope.pageChanged = function () {
                    $scope.currentPage = this.currentPage;

                    views[$scope.view]();
                };
            });

            $scope.getClientTypeAhead = function (query) {
                var deferred = $scope.q.defer();
                $scope.clientListCollection.get({
                    search: query
                }, function (data) {
                    deferred.resolve(data.results);
                });
                return deferred.promise;
            };
            $scope.onSelect = function ($item, $model, $label) {
                $scope.selectedUser = $item.id;
            };

        }]);

    app.register.service('promiseService', function ($q, $rootScope) {
        $rootScope.q = $q
    });
});
