from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from drf.user import UserPermissions, RolePermissions, TaskPermissions
from wtsapp.models import User, Role, OpetationLog, TaskPro, Working
from wtsapp.serializers import UserSerializer, LoginSerializer, RoleSerializer, TaskSerializer, WorkSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [UserPermissions,]


    def create(self, request, *args, **kwargs):
        instance = request.user.instance
        OpetationLog(operator=instance, operation_name=instance.username, module='用户管理', operation='新增').save()
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        """
        instance = request.user.instance
        OpetationLog(operator=instance, operation_name=instance.username, module='用户管理', operation='修改').save()
        return super().update(request, *args, **kwargs)

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



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('-id')
    serializer_class = RoleSerializer
    permission_classes = [RolePermissions,]

    def create(self, request, *args, **kwargs):
        instance = request.user.instance
        OpetationLog(operator=instance, module='角色管理', operation='新增').save()
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        """
        instance = request.user.instance
        OpetationLog(operator=instance, operation_name=instance.username,  module='角色管理', operation='修改').save()
        return super().update(request, *args, **kwargs)



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
    }
    filter_backends = (DjangoFilterBackend, )


    def get_queryset(self):

        instance = self.request.user.instance
        if instance.role in ["管理员", "项目负责人"] or self.request.user.instance.role is None:
            queryset = self.queryset
        else:
            queryset = self.queryset.filter(user=instance.id)
        return self.filter_queryset(queryset)



class WorkingViewSet(viewsets.ModelViewSet):
    """
    工时模块
    """
    queryset = Working.objects.all().order_by('-id')
    serializer_class = WorkSerializer
    # permission_classes = [WorkPermissions,]

    def get_queryset(self):

        instance = self.request.user.instance
        if instance.role in ["管理员", "项目负责人"] or self.request.user.instance.role is None:
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
        if not (instance.role in ["管理员", "项目负责人"] or self.request.user.instance.role is None):
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
        if not (instance.role in ["管理员", "项目负责人"] or self.request.user.instance.role is None):
            approve_status = object.approve_status
            if approve_status not in [0, 2]:
                raise ValidationError("在审批未通过或者待审批情况下可以删除。")

        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)
