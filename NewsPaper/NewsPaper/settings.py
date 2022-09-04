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
# DEBUG = False

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
                'news.context_processors.navigate_context',
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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'postgres',
#         'USER': 'sergey',
#         'PASSWORD': 'pas10121973',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

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

# Cashe
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

# Logging
# System colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # Формат вывода сообщений логгера
    'formatters': {
        # Сообщения в консоль
        # DEBUG
        'con_deb': {
            'format': f'{OKGREEN}%(levelname)s::%(asctime)s::%(message)s{ENDC}'
        },
        # INFO
        'con_info': {
            'format': f'{OKCYAN}%(levelname)s::%(asctime)s::%(module)s::%(message)s{ENDC}'
        },
        # WARNING
        'con_warning': {
            'format': f'{WARNING}%(levelname)s::%(asctime)s::%(message)s::%(pathname)s{ENDC}'
        },
        # ERROR, CRITICAL
        'con_error_cr': {
            'format': f'{FAIL}%(levelname)s::%(asctime)s::%(message)s::%(pathname)s::%(exc_info)s{ENDC}'
        },
        # Логирование в файл
        # INFO_FILE
        'file_info_format': {
            'format': f'%(levelname)s::%(asctime)s::%(module)s::%(message)s'
        },
        # ERROR_FILE
        'file_error_format': {
            'format': '%(levelname)s::%(asctime)s::%(message)s::%(pathname)s::%(exc_info)s'
        },
        # SECURITY
        'security': {
            'format': '%(levelname)s::%(asctime)s::%(module)s::%(message)s'
        },
        # Email сообщение
        # MAIL
        'mail': {
            'format': '%(levelname)s : %(asctime)s : %(message)s : %(pathname)s'
        }
    },
    # Фильтрация
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    # Обработчики
    'handlers': {
        # DEBUG в консоль
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'con_deb',
        },
        # INFO в консоль
        'console_info': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'con_info',
        },
        # WARNING в консоль
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'con_warning',
        },
        # ERROR, CRITICAL в консоль
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'con_error_cr',
        },
        # INFO в файл
        'file_info': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'file_info_format',
            'filename': 'general.log'
        },
        # ERROR в файл
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'file_error_format',
            'filename': 'error.log'
        },
        # INFO Security в файл
        'file_security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'security',
            'filename': 'security.log'
        },
        # ERROR на email
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail',
        },
    },
    # Логгеры
    'loggers': {
        # Логгер принимающий все сообщения
        'django': {
            'handlers': [
                'console_debug',
                'console_info',
                'console_warning',
                'console_error',
                'file_info',
            ],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Логгер обрабатывает все сообщения вызванные HTTP-запросами
        'django.request': {
            'handlers': [
                'mail_admins',
                'file_error',
            ],
            'level': 'ERROR',
            'propagate': False,
        },
        # Логгер принимает все сообщения сервера
        'django.server': {
            'handlers': [
                'mail_admins',
                'file_error',
            ],
            'level': 'ERROR',
            'propagate': False,
        },
        # Обрабатывает ошибки, связанные с отображением шаблонов
        'django.template': {
            'handlers': [
                'file_error',
            ],
            'level': 'ERROR',
            'propagate': False,
        },
        # Логгер обрабатывает любые сообщения связанные
        # со взаимодействием кода с базой данных
        'django.db.backends': {
            'handlers': [
                'file_error',
            ],
            'level': 'ERROR',
            'propagate': False,
        },
        # Предоставляет обработчики ошибок, связанных с безопасностью
        'django.security': {
            'handlers': [
                'file_security',
            ],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
# Отправка почты логгерами
ADMINS = (
    ('admin', os.getenv('EMAIL_YA')),
)
EMAIL_SUBJECT_PREFIX = '[SuperService] '
SERVER_EMAIL = DEFAULT_FROM_EMAIL
