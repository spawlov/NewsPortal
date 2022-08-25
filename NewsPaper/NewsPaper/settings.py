"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

load_dotenv(find_dotenv())
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'news.apps.NewsConfig',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',
    'allauth.socialaccount.providers.vk',
    'django_apscheduler',
    ]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Barnaul'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# SMTP providers
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Yandex
# EMAIL = os.getenv('EMAIL_YA')
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = os.getenv('EMAIL_LOGIN_YA')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD_YA')
# EMAIL_USE_SSL = True
# EMAIL_TIMEOUT = 60

# GMail
# EMAIL = os.getenv('EMAIL_GMAIL')
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = os.getenv('EMAIL_LOGIN_GMAIL')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD_MAIL')
# EMAIL_TIMEOUT = 60

# Mail.ru
EMAIL = os.getenv('EMAIL_MAIL')
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.getenv('EMAIL_LOGIN_MAIL')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD_MAIL')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 60


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allauth
ACCOUNT_FORMS = {'signup': 'news.form.BasicSignupForm'}
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_FORMS = {'signup': 'news.form.SocialSignupForm'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
DEFAULT_FROM_EMAIL = EMAIL
LOGIN_REDIRECT_URL = '/'

# Session time - seconds
SESSION_COOKIE_AGE = 86_400 * 7

# Лимит публикаций за сутки
DAILY_POST_LIMIT = 30

# APScheduler
# формат даты, которую будет воспринимать наш задачник
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
# если задача не выполняется за 25 секунд, то она автоматически
# снимается, можете поставить время побольше, но как правило,
# это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25

# Celery & Redis
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE
