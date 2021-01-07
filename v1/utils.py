# -*- encoding: utf-8 -*-
"""
@File    : utils.py
@Time    : 2020/12/30 14:40
@Author  : wuhao
"""


def check_permission(instance):
    name = instance.role.name.strip() if instance.role else ''
    return name in ["管理员", "项目负责人"] or instance.role is None
