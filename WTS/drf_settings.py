# -*- encoding: utf-8 -*-
"""
@File    : drf_settings.py
@Time    : 2020/12/30 14:28
@Author  : wuhao
"""

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S%z'

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'v1.drf_utils.permissions.MyBasePermission',
        'rest_framework.permissions.IsAuthenticated'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'v1.drf_utils.authentication.JwtTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'v1.drf_utils.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': DATETIME_FORMAT,
    'EXCEPTION_HANDLER': 'v1.drf_utils.exceptionhandler.exception_handler',
    # 'DEFAULT_SCHEMA_CLASS': 'v1.drf_utils.schemas.BaseSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

JWT_CONFIG = {
    'access_token_secret': 'f2b617f1cbc24c399f212bc31bdbdaec',
    'access_token_expires': 2592000,     #　一个月
    'access_token_leeway': 60,     # 在过期时间之后的60s内也可以使用
    'refresh_token_secret': 'a426bfad1bfe42a892a08880485d35f9',
    'user_password_salt': 'bef21f8f341642b1844d083d328b9ab7',
    'refresh_token_expires': 15552000,
    'refresh_token_leeway': 600,
    'mongo_doc_ttl': 2592000,
    'jwt_header': {
        'alg': 'HS256',
        'typ': 'JWT'
        },
    'random_verify_code':{
        'secret': '0e85beefe06b45d78c47bb9ab5389c7d',
        'expire': 600
        },
    }
