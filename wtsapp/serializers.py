# -*- encoding: utf-8 -*-
"""
@File    : serializers.py
@Time    : 2020/12/30 15:54
@Author  : wuhao
"""
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.fields import CharField, IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from v1.drf_utils.auth import create_token
from wtsapp.models import User, Role, TaskPro, Working


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ()

    def create(self, validated_data):
        username = validated_data['username']
        pwd = validated_data['password']
        instance = User.objects.create_user(username=username, password=pwd, phone=validated_data["phone"], role=validated_data['role'])
        return instance

    def update(self, instance, validated_data):
        username = validated_data['username']
        pwd = validated_data['password']
        user = User.objects.filter(username=username)
        if not user:
            raise ValidationError("并沒有此用户")
        user = user.last()
        user.set_password(pwd)
        user.save()
        return user


class LoginSerializer(Serializer):  # noqa

    username = CharField(label="用户名",required=False)
    password = CharField(required=True)


    def create(self, validated_data):

        username = validated_data.pop('username', '')
        pwd = validated_data.get('password', '')

        result = User.objects.filter(username=username, status=1)

        if not result.exists():
            raise NotFound('用户不存在，或已被禁用')
        loginuser = result.first()
        if not loginuser.check_password(pwd):
            raise ValidationError("账号或者密码不正确")

        response_data = create_token(
            loginuser.id,
        )
        return response_data

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        exclude = ()

class TaskSerializer(ModelSerializer):
    task_process = SerializerMethodField(help_text="进度", required=False)
    parent_id = IntegerField(help_text="任务父类id")
    user_id = IntegerField(help_text="")
    class Meta:
        model = TaskPro
        fields = ("id", "task_process", "user_id", "task_name", "start_at", "end_at", "task_status", "parent_id" )

    def get_task_process(self, obj):
        try:
            if not obj.children:   # obj 自己是子类
                obj = obj.parent
            children_counts = TaskPro.objects.filter(parent=obj).count()
            success_chids = TaskPro.objects.filter(parent=obj, task_status=2).count()
            percent = success_chids / children_counts
        except ZeroDivisionError:
            return "0.00%"
        return f"{percent:.2%}"


class WorkSerializer(ModelSerializer):
    taskpro_id = IntegerField(help_text="关联任务id")

    class Meta:
        model = Working
        fields = ("id", "taskpro_id", "work_start", "work_end", "approve_status", "approve_time", "fail_reasons", "work_info", "work_time")

