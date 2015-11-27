/*jslint forin: true */

;
(function ($) {
    $.fn.extend({
        mention: function (options) {
            this.opts = {
                users: [],
                delimiter: '@',
                sensitive: true,
                emptyQuery: false,
                queryBy: ['name', 'username'],
                typeaheadOpts: {}
            };

            var queryText = "",
                _text = function (element) {
                    var range = window.getSelection().getRangeAt(0);
                    var preCaretRange = range.cloneRange();
                    preCaretRange.selectNodeContents(element);
                    //Set Query Text
                    queryText = preCaretRange.toString();
                    return queryText;
                },
                getCaretCharacterOffsetWithin = function (element) {
                    var caretOffset = 0;
                    if (typeof window.getSelection != "undefined") {
                        var range = window.getSelection().getRangeAt(0);
                        var preCaretRange = range.cloneRange();
                        preCaretRange.selectNodeContents(element);
                        //Set Query Text
                        queryText = preCaretRange.toString();
                        preCaretRange.setEnd(range.endContainer, range.endOffset);
                        caretOffset = preCaretRange.toString().length;
                    }
                    return caretOffset;
                },
                settings = $.extend({}, this.opts, options),
                _checkDependencies = function () {
                    if (typeof $ == 'undefined') {
                        throw new Error("jQuery is Required");
                    }
                    else {
                        if (typeof $.fn.typeahead == 'undefined') {
                            throw new Error("Typeahead is Required");
                        }
                    }
                    return true;
                },
                _extractCurrentQuery = function (query, caratPos) {
                    var i;
                    for (i = caratPos; i >= 0; i--) {
                        if (queryText[i] == settings.delimiter) {
                            break;
                        }
                    }
                    return queryText.substring(i, caratPos);
                },
                _matcher = function (itemProps) {
                    var i;
                    if (settings.emptyQuery) {
                        var caratPos = getCaretCharacterOffsetWithin(this.$element[0]),
                            q = (queryText.toLowerCase()),
                            lastChar = q.slice(caratPos - 1, caratPos);
                        if (lastChar == settings.delimiter) {
                            return true;
                        }
                    }
                    for (i in settings.queryBy) {
                        if (itemProps[settings.queryBy[i]]) {
                            var item = itemProps[settings.queryBy[i]].toLowerCase(),
                                usernames = (queryText.toLowerCase()).match(new RegExp(settings.delimiter + '\\w+', "g")),
                                j;
                            if (!!usernames) {
                                for (j = 0; j < usernames.length; j++) {
                                    var username = (usernames[j].substring(1)).toLowerCase(),
                                        re = new RegExp(settings.delimiter + item, "g"),
                                        used = ((queryText.toLowerCase()).match(re));

                                    if (item.indexOf(username) != -1 && used === null) {
                                        return true;
                                    }
                                }
                            }
                        }
                    }
                },
                _updater = function (item) {
                    var itemValues = item.split('.'),
                        data = this.query,
                        caratPos = getCaretCharacterOffsetWithin(this.$element[0]),
                        i;
                    for (i = caratPos; i >= 0; i--) {
                        if (queryText[i] == settings.delimiter) {
                            break;
                        }
                    }
                    var replace = queryText.substring(i, caratPos);
                    data = data.replace(replace, '<a class="mention-link" href="#/profile/' + itemValues[0] + '">' + itemValues[1] + '</a>');

                    this.tempQuery = data;
                    return data;
                },
                _sorter = function (items) {
                    if (items.length && settings.sensitive) {
                        var caratPos = getCaretCharacterOffsetWithin(this.$element[0]),
                            currentUser = _extractCurrentQuery(queryText, caratPos).substring(1),
                            i, len = items.length,
                            priorities = {
                                highest: [],
                                high: [],
                                med: [],
                                low: []
                            }, finals = [];
                        if (currentUser.length == 1) {
                            for (i = 0; i < len; i++) {
                                var currentRes = items[i];

                                if ((currentRes.name[0] == currentUser)) {
                                    priorities.highest.push(currentRes);
                                }
                                else if ((currentRes.name[0].toLowerCase() == currentUser.toLowerCase())) {
                                    priorities.high.push(currentRes);
                                }
                                else if (currentRes.name.indexOf(currentUser) != -1) {
                                    priorities.med.push(currentRes);
                                }
                                else {
                                    priorities.low.push(currentRes);
                                }
                            }
                            for (i in priorities) {
                                var j;
                                for (j in priorities[i]) {
                                    finals.push(priorities[i][j]);
                                }
                            }
                            return finals;
                        }
                    }
                    return items;
                },
                _render = function (items) {
                    var that = this;
                    items = $(items).map(function (i, item) {

                        i = $(that.options.item).attr('data-value', item.id + '.' + item.name);

                        var _linkHtml = $('<div />');

                        if (item.image) {
                            _linkHtml.append('<img class="mention_image" src="' + item.image + '"> ');
                        }
                        if (item.name) {
                            _linkHtml.append('<b class="mention_name">' + item.name + '</b>');
                        }
                        if (item.username) {
                            _linkHtml.append('<span class="mention_username"> ' + settings.delimiter + item.username + '</span>');
                        }

                        i.find('a').html(that.highlighter(_linkHtml.html()));
                        return i[0];
                    });

                    items.first().addClass('active');
                    this.$menu.html(items);
                    return this;
                };

            $.fn.typeahead.Constructor.prototype.render = _render;

            return this.each(function () {
                var _this = $(this);
                if (_checkDependencies()) {
                    _this.typeahead($.extend({
                        source: settings.users,
                        matcher: _matcher,
                        updater: _updater,
                        sorter: _sorter,
                        text: _text
                    }, settings.typeaheadOpts));
                }
            });
        }
    });
})(jQuery);
