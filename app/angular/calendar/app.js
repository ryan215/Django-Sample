'use strict';

define(['app'], function (app, calendar) {
    app.register.controller('EventModalCtrl', ['localStorageService', '$scope', '$modalInstance', '$resource', 'event',
        function (localStorageService, $scope, $modalInstance, $resource, event) {

            var eventResource = $resource("http://:url/feed/event/:id/", {
                url: $scope.restURL,
                id: '@id'
            }, {update: { method: 'PUT' }});



            //***DatePicker***
            $scope.event = event;

            $scope.eventTitleClick = function () {
                if ($scope.event.title === 'Untitled event') $scope.event.title = '';
            };
            $scope.eventTitleBlur = function () {
                if ($scope.event.title === '') $scope.event.title = 'Untitled event';
            };
            $scope.openFromDatePicker = function ($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.fromDatePickerOpened = !$scope.fromDatePickerOpened;
            };
            $scope.openUntilDatePicker = function ($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.untilDatePickerOpened = !$scope.untilDatePickerOpened;
            };
            $scope.ok = function () {
                // Let's just return the important information.
                var event = {
                    id: $scope.event.id,
                    title: $scope.event.title,
                    start: $scope.event.start,
                    end: $scope.event.end,
                    allDay: $scope.event.allDay,
                    calendar: $scope.event.calendar,
                    creator: $scope.event.creator
                };
                $modalInstance.close(event);
                if (event.id == null) {
                    $scope.user_id = localStorageService.get('user_id');
                    event.calendar = $scope.user_id;
                    event.creator = $scope.user_id;
                    event.user = $scope.user_id;
                    eventResource.save(event, function () {
                    }, function (error) {
                    });
                }
                else {
                    $scope.user_id = localStorageService.get('user_id');
                    event.user = $scope.user_id;
                    eventResource.update({id: event.id}, event);
                }
            };
            $scope.close = function () {
                $modalInstance.dismiss();
            };
            $scope.delete = function () {
                eventResource.delete({id: event.id}, event);
                $modalInstance.dismiss('delete');
            };

        }]);
    app.register.directive('profileCalendar', ['localStorageService', '$resource', '$modal', 'rest', 'tokenError',
        function (localStorageService, $resource, $modal) {
            return {
                templateUrl: 'calendar/index.html',
                require: '?ngModel',
                link: function ($scope, element, attrs, ngModel) {
                    ngModel.$render = function () {
                        if (ngModel.$viewValue) {
                            $scope.profile_id = ngModel.$viewValue;
                            // Setup Rest
                            $scope.user_id = localStorageService.get('user_id');
                            var calendarCollection = $resource("http://:url/calendar/:id/", {
                                url: $scope.restURL,
                                id: $scope.profile_id
                            });
                            // Fetch calendar data.
                            $scope.calendarEvents = calendarCollection.get(function () {
                                if ($scope.calendarEvents.results.length) {
                                    $scope.events = $scope.calendarEvents.results;
                                    angular.forEach($scope.events, function (value, key) {
                                        value.start = new Date(value.start);
                                        value.end = new Date(value.end);
                                    });
                                    $scope.eventSources.splice(0, 1, $scope.events);
                                }
                            }, $scope.checkTokenError);

                        }
                    };
                    ngModel.$render();
                },
                controller: function ($scope) {
                    $scope.eventSources = [];
                    $scope.events =[];
                    var eventResource = $resource("http://:url/feed/event/:id/", {
                        url: $scope.restURL,
                        id: '@id'
                    }, {update: { method: 'PUT' }});
                    //alert on Drop
                    $scope.alertOnDrop = function (event, dayDelta, minuteDelta, allDay, revertFunc, jsEvent, ui, view) {
                        console.log('Event Droped to make dayDelta ' + dayDelta);
                        console.log(event);
                        var tempEvent = {
                            id: event.id,
                            title: event.title,
                            start: event.start,
                            end: event.end,
                            allDay: event.allDay,
                            calendar: event.calendar,
                            creator: event.creator,
                            user: event.user
                        };
                        eventResource.update({id:event.id}, tempEvent);
                    };
                    //alert on Resize
                    $scope.alertOnResize = function (event, dayDelta, minuteDelta, revertFunc, jsEvent, ui, view) {
                        console.log('Event Resized to make dayDelta ' + minuteDelta);
                        var tempEvent = {
                            id: event.id,
                            title: event.title,
                            start: event.start,
                            end: event.end,
                            allDay: event.allDay,
                            calendar: event.calendar,
                            creator: event.creator,
                            user: event.user
                        };
                        eventResource.update({id:event.id}, tempEvent);
                    };
                    //Change View
                    $scope.changeView = function (view, calendar) {
                        calendar.fullCalendar('changeView', view);
                    };
                    //***Event Modal***
                    $scope.openEventModal = function (event) {
                        if ($scope.user_id == $scope.profile_id) {
                            var now = new Date(),
                                index = $.inArray(event, $scope.events),
                                defaultEvent = {
                                    title: 'Untitled event',
                                    start: new Date(),
                                    end: new Date(now.setHours(now.getHours() + 1)), // Add an hour to end date.
                                    allDay: false
                                },
                                modalInstance = $modal.open({
                                    templateUrl: 'eventModalTemplate.html',
                                    controller: 'EventModalCtrl',
                                    resolve: {
                                        event: function () {
                                            return $.extend({}, defaultEvent, event)
                                        }
                                    }
                                });
                            modalInstance.result.then(function (newEvent) {
                                if (index == -1) {
                                    // This is a new event from the "Create" button.
                                    $scope.events.push(newEvent);
                                    // In case the Rest hasn't responded.
                                    if (!$scope.eventSources.length) {
                                        $scope.eventSources.push($scope.events);
                                    }
                                }
                                else {
                                    // Let's add the ID so we can edit in back end.
                                    $scope.events.splice(index, 1, $.extend({}, newEvent, {id: event.id}));
                                    // Here I would add some sort of backend update
                                }
                            }, function (reason) {
                                if (reason == "delete") {
                                    $scope.events.splice(index, 1);
                                    // Backend Delete
                                }
                                // Else Modal Closed.
                            });
                        }

                    };
                    //config object
                    $scope.calendarConfig = {
                        height: 600,
                        editable: true,
                        header: {
                            left: 'title',
                            center: '',
                            right: 'today prev,next'
                        },
                        eventClick: $scope.openEventModal,
                        eventDrop: $scope.alertOnDrop,
                        eventResize: $scope.alertOnResize
                    };
                }
            }
        }]);
    return app;
});