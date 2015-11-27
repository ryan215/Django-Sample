import os
gettext = lambda s: s



# Go up 1 directory to get to main django project
DJANGO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# Go up 2 directories to get to main project path
PROJECT_PATH = os.path.abspath(os.path.join(DJANGO_PATH, os.pardir))
# Project path contains media and angular path
MEDIA_PATH = os.path.join(PROJECT_PATH, 'app/angular/media')

# Un-Comment this for UserApp
AUTH_USER_MODEL = 'user_app.CustomUser'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),

)

# Sends email to the console for debugging purposes, comment out for production
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(PROJECT_PATH, 'email')

MANAGERS = ADMINS
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'dev_db.sqlite3',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': '',
            'PASSWORD': '',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'everfit',
            'USER': 'root',
            'PASSWORD': 'L00ksyFit',
            'HOST': 'everfit.cyjyoggmxbrg.us-east-1.rds.amazonaws.com',
            'PORT': '',
        }
    }


NOSE_PLUGINS = [
    'widgets.nose_plugins.SilenceSouth',
]
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['dev.liveeverfit.com', 'liveeverfit.com', 'api.liveeverfit.com', 'localhost']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = MEDIA_PATH
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 't(y&s6khivmx&u&p@v3^ux7wfxj(ro+b_*hc08mdn6d0x5uzs4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'middleware.cors_middleware.CorsMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
if DEBUG:
    pass
else:
    MIDDLEWARE_CLASSES += ('middleware.https_middleware.HttpsMiddleware',)

ROOT_URLCONF = 'django_server.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'django_server.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(DJANGO_PATH, "templates"),
)

AUTHENTICATION_BACKENDS = (
    #'user_app.backend.CustomBackend',
    'django.contrib.auth.backends.ModelBackend',
    'user_auth.backend.UserAuthBackend',

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'user_app',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    #My Apps
    'contact',
    'membership',
    'stripe_payments',

    #Imported Apps
    'south',
    'middleware',
    'django_nose',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'corsheaders',
    'taggit',
    'shopify_app',
    'workouts',
    'messages',
    'feed',
    'model_utils',
    'cicu',
    'schedule',
    'relationships',
    'notifications',
    # 'ws4redis',
    # 'websocketsredis',
    # 'chatserver',
    # 'nbash',
)

CORS_ORIGIN_ALLOW_ALL = True

# MISC APP VARIABLES
TOKEN_EXPIRE = True
# Defaults to 14
TOKEN_EXPIRE_DAYS = 14
if TOKEN_EXPIRE:
    token_class ='user_auth.authentication.ExpiringTokenAuthentication'
else:
    token_class = 'user_auth.authentication.TokenAuthentication'

# In Debug mode, djangos browsable api will be activated (up for discussion)
#  allowing developer to log in easily with email and password


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'PAGINATE_BY': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.XMLRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.XMLParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        token_class,
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += ('user_auth.authentication.DebugAuthentication',)

# Registration App
ACCOUNT_ACTIVATION_DAYS = 7

# Testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# This setting is required to override the Django's main loop, when running in
# development mode, such as ./manage runserver
#WSGI_APPLICATION = 'ws4redis.django_runserver.application'
WSGI_APPLICATION = 'websocketsredis.django_runserver.application'

# URL that distinguishes websocket connections from normal requests
WEBSOCKET_URL = '/ws/'

# Set the number of seconds each message shall persited
WS4REDIS_EXPIRE = 3600

import stripe
#test
# stripe.api_key = 'sk_test_NRP2Hc10fIXIHA5gL0RYaEc5'
#live
stripe.api_key = 'sk_live_IYJVN5y5O9ABOgUVwAbhxt3C'

SHOPIFY_API_KEY = '9832a7588f0038c5adedc3cf78a63d6d'
SHOPIFY_API_PASSWORD = 'dcf4f581af6fbebc44fba62bce63abc3'
SHOPIFY_API_SECRET = 'bd59800006bed1e30c95a834ae4b92a1'
SHOPIFY_STORE = "https://9832a7588f0038c5adedc3cf78a63d6d:dcf4f581af6fbebc44fba62bce63abc3@lef-store.myshopify.com/admin"
SHOPIFY_API_SCOPE = ["write_products", "write_products", "write_customers"]

CHARGIFY_SUBDOMAIN = "shopify-lef-store"
CHARGIFY_API_KEY = "A1KbX8aEd9JgR4MEWCwX"
