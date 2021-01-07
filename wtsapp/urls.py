# -*- encoding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2020/12/30 15:51
@Author  : wuhao
"""

from django.urls import include, path
from rest_framework import routers

from wtsapp import views

router = routers.DefaultRouter()

router.register(r'user', views.UserViewSet, basename="userviewset")    # 用戶的基本信息

router.register(r'role', views.RoleViewSet, basename="roleviewset")    # 角色

router.register(r'task', views.TaskViewSet, basename="taskviewset")    # 任务管理
router.register(r'work', views.WorkingViewSet, basename="workingviewset")    # 工时模块

router.register(r'operate', views.OperateLogViewSet, basename="operatelogviewset")    # 操作日志


# 将router 放入django url中
urlpatterns = [
    path('', include(router.urls)),
]