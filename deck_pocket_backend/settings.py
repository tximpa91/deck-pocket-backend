"""
Django settings for deck_pocket_backend project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import firebase_admin
import logging
import django_heroku
from firebase_admin import credentials
from corsheaders.defaults import default_headers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9uox7#=-+mn@(uh^ehzpa$*ylbb)g#7xs6dlee1y5+n%(d7azw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'channels',
    'graphene_django',
    'graphene_subscriptions',
    'corsheaders',
    'rest_framework.authtoken',
    'oauth2_provider',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sslserver',
    'graphql_playground',
    'deck_pocket'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'deck_pocket_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deck_pocket_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = False

USE_TZ = True
DATETIME_FORMAT = "d-m-Y H:i:s"
DATE_FORMAT = "d-m-Y"
TIME_FORMAT = "H:i:s"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ]

}
OAUTH2_PROVIDER_APPLICATION_MODEL = 'deck_pocket.Oauth2ProviderDeckPocket'

OAUTH2_PROVIDER = {
    # this is the list of available scopes

    'SCOPES_BACKEND_CLASS': 'deck_pocket_backend.scope.CustomScopes',

    'SCOPES': {'read': 'Read Scope', 'write': 'Write Scope'},

    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',

    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,
    'REFRESH_TOKEN_GRACE_PERIOD_SECONDS': 15

}
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.join(BASE_DIR), "static")

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'firebase-user',
]

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = '50502347m20330309'  # my gmail password
EMAIL_HOST_USER = 'luisparada364@gmail.com'  # my gmail username
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
FIREBASE_APP = firebase_admin.initialize_app(cred)
GRAPHENE = {
    'MIDDLEWARE': ['deck_pocket.custom_auth.auth_middleware.AuthorizationMiddleware'],
    'SCHEMA': 'deck_pocket_backend.urls.schema',
}

CARD_MARKET_URL = 'https://www.cardmarket.com'


class GraphQLLogFilter(logging.Filter):
    def filter(self, record):
        if 'graphql.error.located_error.GraphQLLocatedError:' in record.msg:
            return False
        return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    # Prevent graphql exception from displaying in console
    'filters': {
        'graphql_log_filter': {
            '()': GraphQLLogFilter,
        }
    },
    'loggers': {
        'graphql.execution.utils': {
            'level': 'WARNING',
            'handlers': ['console'],
            'filters': ['graphql_log_filter'],
        },
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

ASGI_APPLICATION = "deck_pocket_backend.routing.application"

#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'DeckPocket',
            'USER': 'postgres',
            'PASSWORD': 'docker',
            'HOST': 'localhost',
            'PORT': '5432',
        }

    }
else:
    django_heroku.settings(locals())
