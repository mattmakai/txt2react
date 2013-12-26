import os
from os import environ
from os.path import abspath, basename, dirname, join, normpath
from sys import path

from django.core.exceptions import ImproperlyConfigured
import dj_database_url


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        var_set = environ[setting]
        if var_set == 'true' or var_set == 'True':
            return True
        elif var_set == 'false' or var_set == 'False':
            return False
        return var_set
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


DJANGO_ROOT = dirname(abspath(__file__))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = basename(DJANGO_ROOT)
path.append(DJANGO_ROOT)
DEBUG = get_env_setting("DEBUG")
PRODUCTION_MODE = get_env_setting('PRODUCTION_MODE')
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Matt Makai', 'matthew.makai@gmail.com'),
)
MANAGERS = ADMINS
DATABASES = {'default': \
    dj_database_url.config(default=get_env_setting("DATABASE_URL"))}
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))
STATIC_URL = get_env_setting('STATIC_URL')
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = get_env_setting('SECRET_KEY')

FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'core.context_processors.production_mode',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
)


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION

AUTH_PROFILE_MODULE = 'payments.Customer'

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'gunicorn',
    'south',
    'social_auth',
    'underwear',
)

LOCAL_APPS = (
    'core',
    'payments',
    'reactions',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
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
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'txt2react.wsgi.application'
########## END WSGI CONFIGURATION

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION

if os.getenv('USE_DEBUG_TOOLBAR', False):
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

# Django Social Auth
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
)
GITHUB_APP_ID = get_env_setting('GITHUB_APP_ID')
GITHUB_API_SECRET = get_env_setting('GITHUB_API_SECRET')
TWITTER_CONSUMER_KEY = get_env_setting('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = get_env_setting('TWITTER_CONSUMER_SECRET')
LOGIN_REDIRECT_URL = '/dashboard/'

# security
SESSION_COOKIE_SECURE = get_env_setting('SESSION_COOKIE_SECURE')

