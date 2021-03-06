"""
Django settings for WTS project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
from .drf_settings import *
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*yh!cuwfx=afwp%6ou#%3z37^#yvp2h8(dsay^z+*6h-65(6=1'

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
    'rest_framework',
    'corsheaders',
    'django_filters',
    'wtsapp.apps.WtsappConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True  # 允许ajax跨域请求时携带cookie

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'WTS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'WTS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wts',
        'USER':'root',
        'PASSWORD':'qwe123456',
        'HOST':'localhost',
        'PORT':'3306'
    },
    # 'other': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}

AUTH_USER_MODEL = "wtsapp.User"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans' # 'en-us'

TIME_ZONE = 'Asia/Shanghai' #'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"static"),
]
# 设置收集静态资源的路径(部署时使用)
STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static/')


# 动态资源
MEDIA_DIR=os.path.join(BASE_DIR,'media')
MEDIA_ROOT=MEDIA_DIR
MEDIA_URL='/media/'

X_FRAME_OPTIONS = 'SAMEORIGIN' # django默认值 Deny 不让使用iframe

APPEND_SLASH = False    # 末尾/ 结尾也可识别

# 日志配置
BASE_LOG_DIR = BASE_DIR / "log"
if not BASE_LOG_DIR.exists():
    BASE_LOG_DIR.mkdir()  # 创建路径

LOGGING = {
    'version': 1,    #  dictConfig
    'disable_existing_loggers': False,
    'formatters': {     # 格式化处理
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {
            'format': '%(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'SF': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，根据文件大小自动切
            'filename': os.path.join(BASE_LOG_DIR, "sml.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 备份数为3  xx.log --> xx.log.1 --> xx.log.2 --> xx.log.3
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'TF': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，根据时间自动切
            'filename': os.path.join(BASE_LOG_DIR, "sml.log"),  # 日志文件
            'backupCount': 3,  # 备份数为3  xx.log --> xx.log.2018-08-23_00-00-00 --> xx.log.2018-08-24_00-00-00 --> ...
            'when': 'W0',  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 'error': {
        #     'level': 'ERROR',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
        #     'filename': os.path.join(BASE_LOG_DIR, "MSDApp1_err.log"),  # 日志文件
        #     'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
        #     'backupCount': 5,
        #     'formatter': 'standard',
        #     'encoding': 'utf-8',
        # },
        # 'collect': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
        #     'filename': os.path.join(BASE_LOG_DIR, "MSDApp_collect.log"),
        #     'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
        #     'backupCount': 5,
        #     'formatter': 'collect',
        #     'encoding': "utf-8"
        # }
    },
    'loggers': {
        '': {  # 默认的logger应用如下配置
            'handlers': ['SF', ], # 保留MSDApp1_info.log 文件作为查找数据的依据，
            'level': 'DEBUG',
            'propagate': True,     # 日志是否向上级传递 critical > error > warning > info > debug
        },
    },
    # 'root': {
    #     'handlers': ['console'],
    #     'level': 'DEBUG',
    # },
}