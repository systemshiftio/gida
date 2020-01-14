"""
Django settings for gida project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config
from dj_database_url import parse as db_url
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8hkom9(+%%i(3mb8dt2rlfeuyh%#a!3la8jo!u#@nqru^pa_+q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ['127.0.0.1','gidaafrica.herokuapp.com','gida.africa', 'www.gida.africa']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_registration',
    'waitlist',
    'api',
    'investment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        # 'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 25
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'USER_ID_FIELD': 'id',
}

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = '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'
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT  = 587
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='Systemshift')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='&1pass21?')
# Enable_USE_SSL = True



REST_REGISTRATION = {
    'REGISTER_SERIALIZER_CLASS': 'api.serializers.DefaultRegisterUserSerializer',
    'REGISTER_EMAIL_VERIFICATION_URL': 'http://localhost:3000/reset-password/',
    'REGISTER_SERIALIZER_PASSWORD_CONFIRM': False,
    'REGISTER_VERIFICATION_ENABLED': False,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': True,
    'RESET_PASSWORD_VERIFICATION_URL': 'http://gida.africa:8000/reset-password/',
    'RESET_PASSWORD_VERIFICATION_PERIOD': timedelta(seconds=180),
    'REGISTER_OUTPUT_SERIALIZER_CLASS': 'api.serializers.RegisterToken',

    'VERIFICATION_FROM_EMAIL': 'no-reply@gida.africa',
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


ROOT_URLCONF = 'gida.urls'

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

WSGI_APPLICATION = 'gida.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#         'default':{
#                 'ENGINE':'django.db.backends.postgresql',
#                 'USER': 'nonso',
#                 # 'PASSWORD': "&1pass21",
#                 'NAME': 'gida',
#                 # 'HOST': '139.162.236.179',
#                 # 'PORT': '5432',


#         }
# }

DATABASES = {
    'default': config('DATABASE_URL', default='postgres:///gida', cast=db_url),
}





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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
AUTH_USER_MODEL = "api.GidaUser"

