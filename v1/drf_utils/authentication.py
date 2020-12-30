# -*- encoding: utf-8 -*-
"""
@File    : authentication.py
@Time    : 2020/12/30 14:31
@Author  : wuhao
"""

import time

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from rest_framework.authentication import (
    SessionAuthentication, TokenAuthentication)


#　用户登录后前端在获取到ｔｏｋｅｎ　后存入请求头内AUTHORIZATION
# 类似 AUTHORIZATION : bearer jegitohgjthuojigqwio4uthyy54rejh
from v1.drf_utils.auth import parse_token
from wtsapp.models import AuthUser, User


def authenticate(request):
    authorization = request.META.get('HTTP_AUTHORIZATION') or request.GET.get('Authorization')
    if authorization:
        request.META['HTTP_AUTHORIZATION'] = authorization
    user_info = authorizing(authorization)
    return get_request_instance(user_info)


#　获取token 进行拆分读取token内数据 有则成功登录， 无则失败
def authorizing(authorization):
    token = get_token(authorization)
    if token is None:
        return
    user_info = parse_token(token)
    if user_info is None:
        return
    expire = user_info['exp'] - time.time()
    if expire <= 0:
        return
    return user_info

def get_request_instance(user_info):
    try:
        instance = User.objects.get(id=user_info.get('uId'))
    except Exception:
        return None, None

    if not instance.status:
        return None, None

    return AuthUser(instance, user_info), None


def get_token(authorization):
    """
    从前端获取请求头 取出token
    """
    if authorization is None:
        return
    auth_type = authorization[:7]
    token = authorization[7:].strip()
    if auth_type.lower() != 'bearer ':
        return
    return token

class WrongTokenExcption(exceptions.APIException):
    status_code = 401

class JwtTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        result = authenticate(request)
        if result[0] is None:
            raise WrongTokenExcption('登录超时，请重新登录!!')
        return result

    def enforce_csrf(self, request):
        return