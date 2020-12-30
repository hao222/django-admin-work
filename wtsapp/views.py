from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drf.user import UserPermissions, RolePermissions, TaskPermissions
from wtsapp.models import User, Role, OpetationLog, TaskPro
from wtsapp.serializers import UserSerializer, LoginSerializer, RoleSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [UserPermissions,]


    def create(self, request, *args, **kwargs):
        instance = request.user.instance
        OpetationLog(operator=instance, module='用户管理', operation='新增').save()
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        """
        instance = request.user.instance
        OpetationLog(operator=instance, module='用户管理', operation='修改').save()
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
        OpetationLog(operator=instance, module='角色管理', operation='修改').save()
        return super().update(request, *args, **kwargs)



class TaskViewSet(viewsets.ModelViewSet):
    """
    任务管理模块
    """
    queryset = TaskPro.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    permission_classes = [TaskPermissions,]

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
