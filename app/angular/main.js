/*######################################################
 Set up require.js
 require.js will ensure our dependancies are enforced (recommended by
 the creater of angular). This will allow ease for testing

 Documentation:

 baseUrl: self explanitory
 paths: attach an alias to a path
 Example: 'angular' : '/static/common/js/libs/angular/angular'
 which will look for /static/common/js/libs/angular/angular.js

 using the alias will force modules to make to load
 required alia(s) before doing any sort of code configuration
 Example:
 define(['app', 'angular','common/js/example' ], function(app) {
 ... } //javascript code in here

 app routes to the path /static/app/app.js
 since common/js/example isn't defined in paths
 then require.js will load /static/common/js/example.js
 one time, if example is used more than one place
 then it's better to give it a path

 deps: will initiate the startin depedancies which in term will
 start the real program boostrap.js

 this is a proper definition for shim.
 shim : Configure the dependencies, exports, and custom initialization for older,
 traditional "browser globals" scripts that do not use define() to declare the
 dependencies and set a module value.
 ######################################################*/

require.config({
    baseUrl: "",
    paths: {
        'angular': 'common/angular/angular.min',
        'angularLocalStorage': 'common/angular-local-storage/angular-local-storage',
        'angularResource': 'common/angular-resource/angular-resource.min',
        'angularAMD': 'common/angularAMD/angularAMD.min',
        'ngload': 'common/angularAMD/ngload.min',
        'ngTagsInput': 'common/ng-tags-input/ng-tags-input.min',
        'uiRouter': 'common/angular-ui-router/release/angular-ui-router.min',
        'uiBootstrap': 'common/angular-bootstrap/ui-bootstrap-tpls',
        'routeResolver': 'common/router/routeResolver',
        'autoFillEvent': 'common/autofill-event/src/autofill-event',
        'jquery': 'common/jquery/dist/jquery.min',
        'jqueryui': 'common/jquery-ui/ui/minified/jquery-ui.min',
        'fullcalendar': 'common/fullcalendar/fullcalendar.min',
        'ui.calendar': 'common/angular-ui-calendar/src/calendar',
        'ui.utils': 'common/angular-ui-utils/ui-utils.min',
        'footer': 'footer/app',
        'videojs': 'common/videojs/dist/video-js/video',
        'stripe': 'common/stripe/angular-stripe-js',
        'stripeJS': 'common/stripe/stripe',
        'underscore': 'common/underscore/underscore-min',
        'angular-google-maps': 'common/angular-google-maps/dist/angular-google-maps.min',
        'xeditable': 'common/angular-xeditable/dist/js/xeditable.min',
        'geolocation': 'common/angularjs-geolocation/dist/angularjs-geolocation.min',
        'jcrop': 'common/jcrop/js/jquery.Jcrop.min',
        'angularFileUpload': 'common/ng-file-upload/angular-file-upload.min',
        'angularFileUploadShim': 'common/ng-file-upload/angular-file-upload-shim.min',
        'bootstrap.wysihtml5': 'common/bootstrap3-wysihtml5-bower/dist/amd/bootstrap3-wysihtml5.all',
        'bootstrap.wysihtml5.en-US': 'common/bootstrap3-wysihtml5-bower/dist/locales/bootstrap-wysihtml5.en-US',
        'bootstrap.modal': 'common/bootstrap/js/modal', // I needed this to get the wysihtml5 image and link modals working
        'rangy': 'common/rangy-1.3/rangy-core',
        'masonry': 'common/masonry/dist/masonry.pkgd.min',
        'toasterjs': 'common/angularjs-toaster/toaster',
        'angular-animate': 'common/angular-animate/angular-animate.min',
        'app': 'app',
        'feed': 'feed/app',
        'mention': 'feed/mention',
        'bootstrap-typeahead': 'feed/bootstrap-typeahead',
        'caret': 'feed/jquery.caret.min',
        'calendar': 'calendar/app',
        'socialShare' : 'common/angular-easy-social-share/easy-social-share',
        'mm.foundation' : 'common/mm-foundation/mm-foundation-0.2.2',
        'angular-sanitize' : 'common/angular-sanitize/angular-sanitize',
        'angular-social' : 'common/angular-social/angular-social',
        'infinite-scroll' : 'common/infinite-scroll/ng-infinite-scroll.min'
    },

    //Angular does not support AMD out of the box, put it in a shim
    shim: {
        'angular': {
            exports: 'angular',
            deps: ['angularFileUploadShim']
        },
        'angularAMD': ['angular'],
        'angularLocalStorage': ['angular'],
        'angularResource': ['angular'],
        'uiRouter': ['angular'],
        'uiBootstrap': ['angular'],
        'autoFillEvent': ['angular'],
        'ui.utils': ['angular'],
        'ui.calendar': ['angular'],
        'toasterjs': ['angular-animate'],
        'angular-animate': ['angular'],
        'ngTagsInput': ['angular'],
        'stripe': ['angular', 'stripeJS'],
        'underscore': ['angular'],
        'jqueryui': ['jquery'],
        'fullcalendar': ['jquery'],
        'angular-google-maps': ['angular', 'underscore'],
        'footer': ['app'],
        'xeditable': ['angular'],
        'geolocation': ['angular'],
        'angularFileUpload': ['angular'],
        'jcrop': ['jquery'],
        'masonry': ['jquery'],
        'caret': ['jquery'],
        'bootstrap.modal': ['jquery'],
        'mention': ['jquery', 'bootstrap-typeahead'],
        'bootstrap-typeahead': ['jquery'],
        'bootstrap.wysihtml5': ['jquery', 'rangy','bootstrap.modal'],
        'bootstrap.wysihtml5.en-US': ['bootstrap.wysihtml5'],
        'feed': ['app'],
        'calendar': ['app'],
        'socialShare': ['angular'],
        'mm.foundation' : ['angular'],
        'angular-sanitize' : ['angular'],
        'angular-social' : ['angular'],
        'infinite-scroll' : ['angular']
    },
    // Version the app to avoid cache issues
    urlArgs: "0.0.34",
    waitSeconds: 200,
    // Kick start application
    deps: ['app']
});


