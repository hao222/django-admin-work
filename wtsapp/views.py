import ast
import datetime

from django.db.models import Count, Q
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drf.user import UserPermissions, RolePermissions, TaskPermissions
from v1.utils import check_permission
from wtsapp.models import User, Role, OpetationLog, TaskPro, Working
from wtsapp.serializers import UserSerializer, LoginSerializer, RoleSerializer, TaskSerializer, WorkSerializer, \
    LogoutSerializer, ApproveSerializer, OpetationLogSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [UserPermissions,]
    filterset_fields = {
        'status': ['exact'],
        'username': ['exact']
    }
    filter_backends = (DjangoFilterBackend, )

    def create(self, request, *args, **kwargs):
        instance = request.user.instance
        OpetationLog(operator=instance, operation_name=instance.username, module='用户管理', operation='新增').save()
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        """
        instance = request.user.instance
        OpetationLog(operator=instance, operation_name=instance.username, module='用户管理', operation='修改').save()
        return viewsets.ModelViewSet.update(self, request, *args, **kwargs)

    @action(
        methods=['post'], detail=False, url_path='login', url_name='login',
        authentication_classes=(), permission_classes=(), serializer_class=LoginSerializer)
    def login(self, request):
        """
        登录
        :param request:
        :return:
        """
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.create(serializer.validated_data)
        return Response(response_data)


    @action(methods=['post'], detail=False, url_path='logout',
            url_name='logout', serializer_class=LogoutSerializer)
    def logout(self, request):
        """登出接口"""
        LogoutSerializer.logout(request.META.get('HTTP_AUTHORIZATION'))
        return Response({})

class RoleViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    不允许删除
    """

    queryset = Role.objects.all().order_by('-id')
    serializer_class = RoleSerializer
    permission_classes = [RolePermissions,]
    filterset_fields = {
        'name': ['contains']
    }
    filter_backends = (DjangoFilterBackend, )

    def create(self, request, *args, **kwargs):
        instance = request.user.instance
        OpetationLog(operator=instance, module='角色管理', operation='新增').save()
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        """
        instance = request.user.instance
        OpetationLog(operator=instance, operation_name=instance.username,  module='角色管理', operation='修改').save()
        return viewsets.ModelViewSet.update(self, request, *args, **kwargs)



class TaskViewSet(viewsets.ModelViewSet):
    """
    任务管理模块
    """
    queryset = TaskPro.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    permission_classes = [TaskPermissions,]
    filterset_fields = {
        'task_status': ['exact', 'in'],
        'parent_id': ['isnull', 'exact'],  # 简易版django filters  filter-set
        'task_name': ['exact']
    }
    filter_backends = (DjangoFilterBackend, )


    def get_queryset(self):

        instance = self.request.user.instance
        if check_permission(instance):
        # if instance.role.name.strip() in ["管理员", "项目负责人"] or self.request.user.instance.role is None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(user=instance.id)
        return self.filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        """ 创建任务 """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['creator'] = request.user.instance.username
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def destroy(self, request, *args, **kwargs):
    #     """
    #     删除操作  当父任务删除的时候，子任务所有都要删除
    #     """
    #
    #     instance = self.get_object()
    #     if not instance.parent_id:
    #         # 筛选所有子任务
    #         instance.children.delete()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)



class WorkingViewSet(viewsets.ModelViewSet):
    """
    工时模块
    """
    queryset = Working.objects.all().order_by('-id')
    serializer_class = WorkSerializer
    # permission_classes = [WorkPermissions,]

    def get_queryset(self):

        instance = self.request.user.instance
        if check_permission(instance):
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(taskpro__user=instance.id)
        return self.filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        """
        创建 工时  任何人都可以创建工时
        """
        instance = request.user.instance
        OpetationLog(operator=instance, module='工时管理', operation_name=instance.username, operation='新增').save()
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        """
        修改编辑工时
            条件：
            个人只有在审批未通过或者待审批情况下可以修改
        """
        instance = request.user.instance
        object = self.get_object()
        OpetationLog(operator=instance, operation_name=instance.username, module='工时管理', operation='修改').save()
        if check_permission(instance):
            approve_status = object.approve_status
            if approve_status not in [0, 2]:
                raise ValidationError("在审批未通过或者待审批情况下可以修改。")

        return viewsets.ModelViewSet.update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        删除功能 直接删除
            条件：
            个人只有在审批未通过或者待审批情况下可以修改
        """
        instance = request.user.instance
        object = self.get_object()
        OpetationLog(operator=instance, operation_name=instance.username, module='工时管理', operation='删除').save()
        if check_permission(instance):
            approve_status = object.approve_status
            if approve_status not in [0, 2]:
                raise ValidationError("在审批未通过或者待审批情况下可以删除。")

        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)

    @action(methods=['put'], detail=True, url_path='approve',
            url_name='approve', serializer_class=ApproveSerializer)
    def approve(self, request, pk=None):
        """审批"""

        instance = request.user.instance
        object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        serializer.status_update(object, validated_data)

        return Response(serializer.data)


    @action(methods=['get'], detail=False, url_path='dash_count',
            url_name='dash_count', serializer_class=ApproveSerializer)
    def dash_count(self, request, pk=None):
        """
        首页统计 用户工时通过量
        用户 待审批量 审批通过量 未通过量
        """

        works_user = Working.objects.values("taskpro__user").annotate(
                                            pending=Count("id", filter=Q(approve_status=0)), approve=Count("id",
                                    filter=Q(approve_status=1)), not_pass=Count("id", filter=Q(approve_status=2))).values("taskpro__user__username", "pending", "approve", "not_pass")
        works_all = {}
        works_all['pending'] = [sum(x.get('pending') for x in works_user if x.get("pending"))][0]
        works_all['approve'] = [sum(x.get('approve') for x in works_user if x.get("approve"))][0]
        works_all['not_pass'] = [sum(x.get('not_pass') for x in works_user if x.get("not_pass"))][0]
        users_name = [x.get("taskpro__user__username") for x in works_user]

        status_user = {"pending": [x.get('pending', 0) for x in works_user], 'approve': [x.get('approve', 0) for x in works_user], 'not_pass': [x.get('not_pass', 0) for x in works_user]}
        return Response({"works_user": status_user, "users_name": users_name, "works_all": works_all, "response": "ok"})

class OperateLogViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    操作日志
    """
    queryset = OpetationLog.objects.all().order_by('-id')
    serializer_class = OpetationLogSerializer

    filterset_fields = {
        'operation_name': ['exact']
    }
    filter_backends = (DjangoFilterBackend, )