# -*- encoding: utf-8 -*-
"""
@File    : user.py
@Time    : 2020/12/30 16:35
@Author  : wuhao
"""
from rest_framework import permissions

from v1.utils import check_permission


class BaseViewsPermissions(permissions.BasePermission):
    """  """

    def has_permission(self, request, view):
        """ 判断是否拥有权限 """
        action = view.action

        has_permission_action = 'has_permission_' + action
        if hasattr(self, has_permission_action):
            return getattr(self, has_permission_action)(request, view)
        return True



class UserPermissions(BaseViewsPermissions):
    """ Userviewset """
    @staticmethod
    def has_permission_list(request, view):
        if request.user:
            return True
        return False

    @staticmethod
    def has_permission_create(request, view):
        if request.user:
            if check_permission(request.user.instance):
                return True
            return False
        return False


class RolePermissions(BaseViewsPermissions):
    """ Userviewset """
    @staticmethod
    def has_permission_list(request, view):
        if request.user:
            return True
        return False

    @staticmethod
    def has_permission_create(request, view):
        if request.user:
            if check_permission(request.user.instance):
                return True
            return False
        return False

    @staticmethod
    def has_permission_delete(request, view):
        if request.user:
            if check_permission(request.user.instance):
                return True
            return False
        return False


class TaskPermissions(BaseViewsPermissions):
    """ Task """

    @staticmethod
    def has_permission_delete(request, view):
        if request.user:
            if check_permission(request.user.instance):
                return True
            return False
        return False

    @staticmethod
    def has_permission_create(request, view):
        if request.user:
            if check_permission(request.user.instance):
                return True
            return False
        return False

    @staticmethod
    def has_permission_update(request, view):
        if request.user:
            if check_permission(request.user.instance):
                return True
            return False
        return False


# class WorkPermissions(BaseViewsPermissions):
#     """ Task """
#
#     @staticmethod
#     def has_permission_delete(request, view):
#         if request.user:
#             if request.user.instance.role in ["管理员", "项目负责人"] or request.user.instance.role is None:
#                 return True
#             return False
#         return False
#
#     @staticmethod
#     def has_permission_create(request, view):
#         if request.user:
#             if request.user.instance.role in ["管理员", "项目负责人"] or request.user.instance.role is None:
#                 return True
#             return False
#         return False
#
#     @staticmethod
#     def has_permission_update(request, view):
#         if request.user:
#             if request.user.instance.role in ["管理员", "项目负责人"] or request.user.instance.role is None:
#                 return True
#             return False
#         return False
