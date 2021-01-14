"""
Django settings for WMS project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# Membaca file .env
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+)@%&4jov_djsuvy+(a-b4px8&w*!st%46&evv92c1(8&+f_9p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'WMS',
    'wmsInbound',
    'wmsOutbound',
    'wmsStorage',
    'wmsReturn',
    'sequences.apps.SequencesConfig'
    # 'category',
    # 'storage',
    # 'outbound',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# SESSION_EXPIRE_SECONDS = 60 * 20

# SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# SESSION_TIMEOUT_REDIRECT = 'login'

ROOT_URLCONF = 'WMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'WMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'd699g0o727nj4n',
#         'USER': 'nogtyfdvvarzgu',
#         'PASSWORD': '5f3a888811135823c86716b44c6c40bd93aee46161ce83ff94ed275746039eee',
#         'HOST': 'ec2-34-238-26-109.compute-1.amazonaws.com'
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd636rfnio6olin',
        'USER': 'tltgafsivdcprs',
        'PASSWORD': '1fbf8b847b21a32bbe6aef2f6c1c9286fd1c5dce58ac703f7081d2e0ac319262',
        'HOST': 'ec2-54-243-67-199.compute-1.amazonaws.com'
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'DBWMSLoc',
#         'USER': 'postgres',
#         'PASSWORD': 'admin',
#         'HOST': '127.0.0.1'
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#------------ Email --------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER='wmspoltekpos@gmail.com'
DEFAULT_FROM_EMAIL='wmspoltekpos@gmail.com'
EMAIL_HOST_PASSWORD='wmspoltekpos17'
EMAIL_HOST='smtp.gmail.com'
EMAIL_USE_TLS=True
EMAIL_PORT=587

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = 'mymedia'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
