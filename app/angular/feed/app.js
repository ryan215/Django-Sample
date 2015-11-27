'use strict';

define(['app', 'masonry'], function (app, Masonry) {
    app.register.directive('entryFeed', ['$modal', '$resource', '$upload', '$sce', '$sanitize', '$location', '$window',  'rest', 'localStorageService', 'fileReader', 'tokenError',
        function ($modal, $resource, $upload, $sce, $sanitize, $location,  $window, rest, localStorageService, fileReader, tokenError) {
            return {
                templateUrl: 'feed/index.html',
                require: '?ngModel',
                link: function ($scope, element, attrs, ngModel) {
                    angular.extend($scope, {
                            user_id: localStorageService.get('user_id'),
                            user_email: localStorageService.get('user_email'),
                            usrImg: localStorageService.get('user_img'),
                            entryInputPlaceHolder: $sce.trustAsHtml("Type what’s on your mind here..."),
                            entryInputText: "",
                            entryVideoURL: "",
                            entryBlogBody: "",
                            entryVideoURLID: "",
                            entryTags: [],
                            tags: undefined,
                            entryInputType: "text",
                            fromDatePickerOpened: false,
                            untilDatePickerOpened: false,
                            page : 1,
                            loadSpecialty: function (query) {
                                var tagTemp, deferred;
                                deferred = $scope.q.defer();
                                if(query) {
                                    tagTemp = $scope.tagCollection.get({search:query}, function(){
                                        deferred.resolve(tagTemp.results);
                                    });
                                }
                                return deferred.promise;
                            },
                            entryEvent: {
                                start: "",
                                end: "",
                                allDay: false
                            },
                            likeEntry: function (entry) {
                                $scope.likeResource.update({
                                    id: entry.id,
                                    user_id: $scope.user_id
                                }, function (data) {
                                    if (data.user_likes == 'true') {
                                        entry.user_likes = true;
                                        entry.likes += 1;
                                    } else {
                                         entry.user_likes = false;
                                        entry.likes -= 1;
                                    }
                                    ;
                                });
                            },
                            getTrustedURL: function (url) {
                                return $sce.trustAsResourceUrl(url);
                            },
                            getTrustedHtml: function (html, truncate) {
                                if (html && truncate) {
                                    var inputWords = html.split(/\s+/);
                                    if (html.length > 21) {
                                        html = inputWords.slice(0, 21).join(' ') + '...<br>';
                                    }
                                }
                                return $sce.trustAsHtml(html.replace(/(http[^\s]+)/, '<a href="$1">$1</a>'));
                            },
                            readMore: function (entry) {
                                entry.expand = true;
                                $scope.refreshMasonry();
                            },
                            runMasonry: function () {
                                if ($scope.msnry)$scope.msnry.destroy();
                                setTimeout(function () {
                                    $scope.msnry = new Masonry(".newsFeed .row", {
                                        columnWidth: '.grid-sizer',
                                        itemSelector: '.item',
                                        transitionDuration: '0.2s'
                                    });
                                }, 3);
                            },
                            refreshMasonry: function () {
                                setTimeout(function () {
                                    $scope.msnry.layout();
                                }, 3);
                            },
                            entryYouTubeChange: function () {
                                $scope.refreshMasonry();
                                if ($scope.entryVideoURL) {
                                    if ($scope.entryVideoURL.indexOf("watch?v=") > -1) {
                                        $scope.entryVideoURLID = '//www.youtube.com/embed/' + this.entryVideoURL.slice(this.entryVideoURL.indexOf("watch?v=") + 8)
                                        $scope.entryVideoURLIDTrusted = $sce.trustAsResourceUrl(this.entryVideoURLID);
                                        return;
                                    }
                                    else if ($scope.entryVideoURL.indexOf("http://youtu.be/") > -1) {
                                        $scope.entryVideoURLID = '//www.youtube.com/embed/' + this.entryVideoURL.slice(this.entryVideoURL.indexOf("youtu.be/") + 9);
                                        $scope.entryVideoURLIDTrusted = $sce.trustAsResourceUrl(this.entryVideoURLID);
                                        return;
                                    }
                                    else if ($scope.entryVideoURL.indexOf("embed/") > -1) {
                                        $scope.entryVideoURLID = '//www.youtube.com/embed/' + this.entryVideoURL.slice(this.entryVideoURL.indexOf("embed/") + 6);
                                        $scope.entryVideoURLIDTrusted = $sce.trustAsResourceUrl(this.entryVideoURLID);
                                        return;
                                    }
                                }
                                $scope.entryVideoURLID = $scope.entryVideoURLIDTrusted = '';
                            },
                            openFromDatePicker: function ($event) {
                                $event.preventDefault();
                                $event.stopPropagation();
                                this.fromDatePickerOpened = !this.fromDatePickerOpened;
                            },
                            openUntilDatePicker: function ($event) {
                                $event.preventDefault();
                                $event.stopPropagation();
                                this.untilDatePickerOpened = !this.untilDatePickerOpened;
                            },
                            entryAffiliate: function (where) {
                                var i,
                                theLink,
                                pageLink = encodeURIComponent($location.absUrl()+ "profile/" + $scope.user_id + '?referral=' + $scope.user_email),
                                pageTitleUri = encodeURIComponent('Check my page out on Liveeverfit! '),
                                shareLinks = [];
                                console.log(pageLink);
                                switch (where) {
                                    case 'twitter':
                                      theLink = 'http://twitter.com/intent/tweet?text=' + pageTitleUri + '%20' + pageLink;
                                      break;
                                    case 'facebook':
                                      theLink = 'http://facebook.com/sharer.php?u=' + pageLink;
                                      break;
                                    case 'linkedin':
                                      theLink = 'http://www.linkedin.com/shareArticle?mini=true&url=' + pageLink + '&title=' + pageTitleUri;
                                      break;
                                }
                                $window.open(theLink);

                            },
                            entryTransformation: function() {
                                $scope.entryTags.push({name: 'transformation'});
                            },
                            shareEntryMention: function (index) {
                                $scope.shareEntryInputText = $scope.shareEntryInputText.concat('@');
                                setTimeout(function () {
                                    var input = $('#entryShareInput'+index),
                                        range = document.createRange(),
                                        sel = window.getSelection();

                                    range.selectNodeContents(input[0]);
                                    range.collapse(false);
                                    sel.removeAllRanges();
                                    sel.addRange(range);
                                    input.focus().keyup();
                                });
                            },
                            entryMention: function () {
                                $scope.entryInputText = $scope.entryInputText.concat('@');
                                setTimeout(function () {
                                    var input = $('#entryInput'),
                                        range = document.createRange(),
                                        sel = window.getSelection();

                                    range.selectNodeContents(input[0]);
                                    range.collapse(false);
                                    sel.removeAllRanges();
                                    sel.addRange(range);
                                    input.focus().keyup();
                                });
                            },
                            entrySubmit: function () {
                                var scope = this,
                                    runEntrySubmit = {
                                        entryCollection: $resource(":protocol://:url/feed/:type", {
                                            type: $scope.entryInputType,
                                            protocol: $scope.restProtocol,
                                            url: $scope.restURL
                                        }, {
                                            update: {
                                                method: 'PUT'
                                            }
                                        }),
                                        text: function () {
                                            this.entryCollection.save({
                                                text: $scope.entryInputText,
                                                user: $scope.user_id,
                                                tags: $scope.entryTags
                                            }, function (data) {
                                                $scope.feedList.unshift(data);
                                                $scope.entryInputText = '';
                                                $scope.runMasonry();
                                                $scope.entryTags = [];
                                            });
                                        },
                                        photo: function () {
                                            if ($scope.uploadImg) {
                                                $scope.upload = $upload.upload({
                                                    url: $scope.restProtocol + '://' + $scope.restURL + '/feed/photo',
                                                    data: {
                                                        user: $scope.user_id,
                                                        text: $scope.entryInputText,
                                                        tags: $scope.entryTags
                                                    },
                                                    file: $scope.uploadImg,
                                                    fileFormDataName: 'img'
                                                }).progress(function (evt) {
                                                    $scope.percent = parseInt(100.0 * evt.loaded / evt.total);
                                                }).success(function (data) {
                                                    $scope.feedList.unshift(data);
                                                    $scope.entryInputText = '';
                                                    $scope.runMasonry();
                                                    delete $scope.uploadImg;
                                                    delete $scope.entryImgSrc;
                                                    setTimeout(function() {
                                                        $scope.$apply(function() {
                                                            $scope.percent = scope.percent = false;
                                                        });
                                                    });
                                                    $scope.entryTags = [];
                                                }).error(function (data) {
                                                    $scope.percent = false;
                                                    console.log("Upload photo error.")
                                                });
                                            }
                                            else {
                                                // Some sort of error.
                                                console.log("No file selected.")
                                            }
                                        },
                                        video: function () {
                                            if ($scope.entryVideoURLID) {
                                                this.entryCollection.save({
                                                    text: $scope.entryInputText,
                                                    url: $scope.entryVideoURLID,
                                                    user: $scope.user_id,
                                                    tags: $scope.entryTags
                                                }, function (data) {
                                                    $scope.feedList.unshift(data);
                                                    $scope.entryInputText = '';
                                                    $scope.entryVideoURL = "";
                                                    $scope.entryVideoURLID = "";
                                                    $scope.entryVideoURLIDTrusted = "";
                                                    $scope.runMasonry();
                                                    $scope.entryTags = [];
                                                })
                                            } else {
                                                $scope.entryVideoURL = "";
                                            }
                                        },
                                        event: function () {
                                            if ($scope.entryEvent.start && $scope.entryEvent.end) {
                                                this.entryCollection.save({
                                                    title: $scope.entryInputText,
                                                    start: $scope.entryEvent.start,
                                                    end: $scope.entryEvent.end,
                                                    allDay: $scope.entryEvent.allDay,
                                                    user: $scope.user_id,
                                                    tags: $scope.entryTags,
                                                    creator : $scope.user_id
                                                }, function (data) {
                                                    $scope.feedList.unshift(data);
                                                    $scope.entryInputText = '';
                                                    $scope.entryTags = [];
                                                    $scope.entryEvent = {
                                                        start: "",
                                                        end: "",
                                                        allDay: false
                                                    }
                                                    $scope.runMasonry();
                                                });
                                            }

                                        },
                                        blog: function () {
                                            if ($scope.entryBlogBody) {
                                                this.entryCollection.save({
                                                    text: $scope.entryInputText,
                                                    body: $scope.entryBlogBody,
                                                    user: $scope.user_id,
                                                    tags: $scope.entryTags
                                                }, function (data) {
                                                    $scope.feedList.unshift(data);
                                                    $scope.entryInputText = '';
                                                    $scope.entryBlogBody = '';
                                                    $scope.runMasonry();
                                                    $scope.entryTags = [];
                                                });
                                            }
                                            else {
                                                $scope.entryBlogBody = "<b>Type the title of greatness for your Blog here...</b>";
                                                setTimeout(function () {
                                                    $scope.entryBlogBody = "";
                                                }, 300);
                                            }
                                        }
                                    };
                                if ($scope.entryInputText || $scope.uploadImg || $scope.entryVideoURLID) {
                                    runEntrySubmit[$scope.entryInputType]();
                                } else {
                                    $scope.entryInputPlaceHolder = $sce.trustAsHtml("<b>Type something here...</b>");
                                    setTimeout(function () {
                                        $scope.entryInputPlaceHolder = $sce.trustAsHtml("Post an update...");
                                    }, 300);
                                }
                            },
                            socialShareEntry: function (entry, where) {
                                var i,
                                theLink,
                                pageLink = encodeURIComponent($location.absUrl()+ "entry/" + entry.id + '?referral=' + $scope.user_email),
                                pageTitleUri = encodeURIComponent('Join us at Liveeverfit!'),
                                shareLinks = [];
                                switch (where) {
                                    case 'twitter':
                                      theLink = 'http://twitter.com/intent/tweet?text=' + pageTitleUri + '%20' + pageLink;
                                      break;
                                    case 'facebook':
                                      theLink = 'http://facebook.com/sharer.php?u=' + pageLink;
                                      break;
                                    case 'linkedin':
                                      theLink = 'http://www.linkedin.com/shareArticle?mini=true&url=' + pageLink + '&title=' + pageTitleUri;
                                      break;
                                }
                                $window.open(theLink);

                            },
                            previousShareEntry: null,
                            entryShare: function(entry) {
                                if($scope.previousShareEntry) $scope.previousShareEntry.showShareEntryInput = false;
                                $scope.previousShareEntry = entry;
                                entry.showShareEntryInput = true;
                                $scope.refreshMasonry();
                            },
                            shareEntrySubmit: function (entry) {
                                var id,
                                    entryCollection = $resource(":protocol://:url/feed/shared", {
                                        protocol: $scope.restProtocol,
                                        url: $scope.restURL
                                    }, {
                                        update: {
                                            method: 'PUT'
                                        }
                                    });

                                if (entry.type == 'shared') {
                                    id = entry.shared_entry.id;
                                } else {
                                    id = entry.id;
                                }

                                entryCollection.save({
                                        user: $scope.user_id,
                                        entry: id,
                                        text: $scope.shareEntryInputText,
                                        tags: $scope.shareEntryTags
                                    },
                                    function (data) {
                                        if($scope.previousShareEntry) $scope.previousShareEntry.showShareEntryInput = false;
                                        $scope.shareEntryInputText = "";
                                        $scope.shareEntryTags = [];
                                        $scope.feedList.unshift(data);
                                        $scope.runMasonry();
                                    });
                            },
                            selectEntryInputType: function (type) {
                                $scope.entryInputType = type;
                                $scope.refreshMasonry();
                                $scope.entryImgSrc = '';
                                if (type == 'event') {
                                    $scope.entryInputPlaceHolder = $sce.trustAsHtml("Type your awesome event here...");
                                    $scope.entryInputText = '';
                                } else if (type == 'blog') {
                                    $scope.entryInputPlaceHolder = $sce.trustAsHtml("Type the title of greatness for your Blog here...");
                                    $scope.entryInputText = '';
                                } else if (type == 'video') {
                                    $scope.entryInputPlaceHolder = $sce.trustAsHtml("Type your video title here...");
                                    $scope.entryInputText = '';
                                } else if (type == 'photo') {
                                    $scope.entryInputPlaceHolder = $sce.trustAsHtml("Type the title of your photo here...");
                                    $scope.entryInputText = '';
                                }
                                else {
                                    $scope.entryInputPlaceHolder = $sce.trustAsHtml("Type what’s on your mind here...");
                                }
                            },
                            onFileSelect: function ($files) {
                                $scope.uploadImg = $files[0];
                                $scope.refreshMasonry();
                                fileReader.readAsDataUrl($scope.uploadImg, $scope).then(function (result) {
                                    $scope.entryImgSrc = result;
                                    $scope.percent = undefined;
                                    $scope.runMasonry();
                                });
                            },
                            deleteEntry: function (index, entry) {
                                var entryObj = {
                                    id: entry.id,
                                    type: entry.type

                                };
                                $scope.feedList.splice(index, 1);
                                $scope.runMasonry();
                                $scope.entryResource.delete(entryObj, $.noop());
                            },
                            flagEntry: function (entry) {
                                $scope.flagResource.save({
                                    entry: entry.id,
                                    reporter: $scope.user_id
                                }, function () {

                                });
                            },
                            submitComment: function (entry) {
                                var scope = this,
                                    commentObj = {
                                        text: entry.commentInput,
                                        user: $scope.user_id,
                                        entry: entry.id
                                    };
                                $scope.commentResource.save(commentObj, function (data) {
                                    entry.comments.push(data);
                                    setTimeout(function () {
                                        $scope.msnry.layout();
                                    });
                                    entry.commentInput = '';
                                });
                            },
                            deleteComment: function (index, comment, entry) {
                                var commentObj = {
                                    id: comment.id
                                };
                                entry.comments.splice(index, 1);
                                $scope.commentResource.delete(commentObj, function () {

                                });
                            },
                            editComment: function (index, comment) {
                                var attrs;
                                $scope.commentResource.update(comment, function () {

                                });
                            },
                            likeResource: $resource(":protocol://:url/feed/likes/:id", {
                                protocol: $scope.restProtocol,
                                url: $scope.restURL,
                                id: '@id'
                            }, {
                                update: {
                                    method: 'PUT'
                                }
                            }),
                            // Get list of entries.
                            feedCollection: $resource(":protocol://:url/feed:filter/:id", {
                                protocol: $scope.restProtocol,
                                url: $scope.restURL,
                                filter: '@filter',
                                id: '@id'
                            }, {
                                update: { method: 'PUT' }
                            }),
                            // For submitting an entry.
                            entryResource: $resource(":protocol://:url/feed/:type/:id", {
                                id: "@id",
                                type: "@type",
                                protocol: $scope.restProtocol,
                                url: $scope.restURL
                            }, {
                                update: { method: 'PUT' }
                            }),
                            commentResource: $resource(":protocol://:url/feed/comment/:id", {
                                id: '@id',
                                protocol: $scope.restProtocol,
                                url: $scope.restURL
                            }, {
                                update: { method: 'PUT' }
                            }),
                            flagResource: $resource(":protocol://:url/feed/flag", {
                                protocol: $scope.restProtocol,
                                url: $scope.restURL
                            }),
                            tagCollection: $resource(":protocol://:url/all-tags/",{
                                protocol: $scope.restProtocol,
                                url: $scope.restURL,
                            },{update: { method: 'PATCH' }}),
                            feedPhotoList: [],
                            openLightbox: function(entry) {
                                $modal.open({
                                    templateUrl: 'feed/lightbox.html',
                                    controller: lightBoxController,
                                    windowClass: 'lightbox',
                                    resolve: {
                                        selected: function() {
                                            return entry
                                        },
                                        feedPhotoList: function() {
                                            return $scope.feedPhotoList;
                                        },
                                        getTrustedHtml: function() {
                                            return $scope.getTrustedHtml
                                        }
                                    }
                                });
                            },
                            getPros : function () {

                                $scope.page = $scope.page + 1;
                                $scope.filtering = {
                                    page: $scope.page,
                                };
                                

                                var newEntries = $scope.feedCollection.get($scope.filtering, function () {
                                    
                                    
                                    $scope.feedList = $scope.feedList.concat(newEntries.results);
                                    $scope.next = newEntries.next;

                                });

                                //$scope.msnry.append('test');
                                
                                //if ($scope.msnry)$scope.msnry.destroy();
                                setTimeout(function () {
                                    
                                    $scope.msnry = new Masonry(".newsFeed .row", {
                                        columnWidth: '.grid-sizer',
                                        itemSelector: '.item',
                                        transitionDuration: '0.2s'
                                    });
                                }, 1000);
                                
                            },
                            shareEntryInputText: "",
                            shareEntryInputPlaceHolder: $sce.trustAsHtml("Post an update..."),
                            shareEntryTags: [],
                            init: function () {
                                $scope.feed_id = ngModel.$viewValue.id;
                                $scope.feedCollection.get({id: $scope.feed_id, filter: ngModel.$viewValue.filter}, function (data) {
                                    $scope.feedList = data.results;
                                    $scope.runMasonry();
                                    angular.forEach(data.results, function (value, key) {
                                        if (value.type == 'photo') {
                                            $scope.feedPhotoList.push(value);
                                        }
                                        else if (value.type == 'shared' && value.shared_entry.type == 'photo') {
                                            $scope.feedPhotoList.push(value.shared_entry);
                                        }
                                    });
                                }, $scope.checkTokenError);
                                if(ngModel.$viewValue.entryTags){
                                    $scope.entryTags = ngModel.$viewValue.entryTags
                                }
                            }
                        }
                    )
                    ;
                    // model -> view
                    if (ngModel) {
                        ngModel.$render = function () {
                            if (ngModel.$viewValue) {
                                $scope.init();
                                $scope.filter = ngModel.$viewValue.filter;
                            }
                        };
                        ngModel.$render();
                    }
                }
            }
        }]);
    var lightBoxController = function ($scope, $modalInstance, selected, feedPhotoList, getTrustedHtml) {
        $scope.images = feedPhotoList;
        $scope.selectedImg = selected;
        $scope.getTrustedHtml = getTrustedHtml;
        $scope.displayImage = function (img) {
            $scope.selected = $scope.images.indexOf(img);
            $scope.selectedImg = img;
        };
        $scope.source = function (img) {
            return '/media/' + img['img'];
        };
        $scope.hasPrev = function () {
            return ($scope.selected !== 0);
        };
        $scope.hasNext = function () {
            return ($scope.selected < $scope.images.length - 1);
        };
        $scope.next = function () {
            $scope.selected = $scope.selected + 1;
            $scope.selectedImg = $scope.images[$scope.selected];
        };
        $scope.prev = function () {
            $scope.selected = $scope.selected - 1;
            $scope.selectedImg = $scope.images[$scope.selected];
        };
        // Init lightbox
        $scope.displayImage(selected);
    };
    return app;
})
