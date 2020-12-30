# -*- encoding: utf-8 -*-
"""
@File    : exceptionhandler.py
@Time    : 2020/12/30 14:32
@Author  : wuhao
"""

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework.views import set_rollback


def _get_detail(detail):
    # 针对返回报错信息的处理 统一为字典形式
    if isinstance(detail, list):
        return ''.join([x if isinstance(x, str) else _get_detail(x) for x in detail])
    result = ''
    for v in detail.values():
        result += _get_detail(v)
    return result


def handler500(*_, **__):
    return Response({'detail': '服务异常，请稍后再试'})


def exception_handler(exc, context):
    '''
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    '''

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            detail = _get_detail(exc.detail)
            data = {'detail': detail, 'sub_detail': exc.detail}
        else:
            data = {'detail': exc.detail, 'sub_detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    return None

