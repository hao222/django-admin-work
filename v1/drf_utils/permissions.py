# -*- encoding: utf-8 -*-
"""
@File    : permissions.py
@Time    : 2020/12/30 14:33
@Author  : wuhao
"""

from rest_framework import permissions

class MyBasePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

