# -*- encoding: utf-8 -*-
"""
@File    : serializers.py
@Time    : 2020/12/30 15:54
@Author  : wuhao
"""
import datetime
import time

from django.core.validators import RegexValidator
from django.db.transaction import atomic
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.fields import CharField, IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from v1.drf_utils.auth import create_token, parse_token
from v1.drf_utils.authentication import get_token
from wtsapp.models import User, Role, TaskPro, Working, OpetationLog

phone_validator = RegexValidator(r"^1[3456789][0-9]{9}$", "请输入正确的手机号码。")


class UserSerializer(ModelSerializer):
    role_name = CharField(source='role.name', read_only=True)

    class Meta:
        model = User
        exclude = ()

    def create(self, validated_data):
        username = validated_data['username']
        pwd = validated_data['password']
        instance = User.objects.create_user(username=username, password=pwd, phone=validated_data["phone"], role=validated_data['role'])
        return instance

    def update(self, instance, validated_data):
        pwd = validated_data.pop("password")
        origin_pwd = instance.password
        object = super().update(instance, validated_data)
        if pwd != origin_pwd:
            object.set_password(pwd)
            object.save()
        return object


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
        if loginuser.role != None and not loginuser.role.status:
            raise ValidationError("角色已禁用")
        response_data = create_token(
            loginuser.id,
        )
        response_data.update(dict(name=loginuser.username))
        # 记录最后登录时间
        now = datetime.datetime.now()
        loginuser.last_login = now
        loginuser.save()
        return response_data

class LogoutSerializer(Serializer):

    @classmethod
    def logout(cls, athorization):
        token = get_token(athorization)
        if token is None:
            raise ValidationError('未登录')
        user_info = parse_token(token)
        expire = user_info['exp'] - time.time()
        if expire <= 0:
            return
        # redis_client.set(TOKEN_REDIS_KEY + token, expire, ex=int(expire) + 1)  # 暂时不做redis缓存处理


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        exclude = ()

class TaskSerializer(ModelSerializer):
    task_process_list = SerializerMethodField(help_text="进度", required=False, read_only=True)
    parent_id = CharField(help_text="任务父类id", required=False, allow_blank=True, allow_null=True)
    user_id = IntegerField(help_text="")
    exect_person = CharField(source="user.username", required=False, read_only=True)
    user_role = CharField(source="user.role.name", required=False, read_only=True)

    class Meta:
        model = TaskPro
        fields = ("id", "task_process", "user_id", "task_name", "start_at", "end_at", "task_status", "parent_id", "exect_person", "creator","user_role", "task_process_list", "task_info" )

    def get_task_process_list(self, obj):
        try:
            process = obj.task_process or '0'
        except Exception:
            return "0%"
        return f"{process}%"


class WorkSerializer(ModelSerializer):
    taskpro_id = IntegerField(help_text="关联任务id")
    task_name = CharField(source="taskpro.task_name", required=False, read_only=True)
    username = CharField(source="taskpro.user.username", required=False, read_only=True)
    role_name = CharField(source="taskpro.user.role.name", required=False, read_only=True)

    class Meta:
        model = Working
        fields = ("id", "taskpro_id", "work_start", "work_end", "approve_status", "approve_time", "reasons", "work_info", "work_time", "task_name", "username", "role_name", "create_at")


class ApproveSerializer(Serializer):
    approve_status = IntegerField(help_text='审批状态 0待审批 1已审批 2未通过')
    reasons = CharField(help_text="一些issues")

    class Meta:
        # 重用WorkSerializer
        model = Working

    def status_update(self, instance, validated_data):
        now = datetime.datetime.now()
        user = self.context['request'].user.instance
        change_person =user.username

        validated_data['approve_time'] = now
        validated_data['approveor'] = change_person
        with atomic():
            instance = WorkSerializer.update(self, instance, validated_data)
            OpetationLog(operator=user, operation_name=change_person, module='工时管理', operation='审批').save()

        return instance

class OpetationLogSerializer(ModelSerializer):


    class Meta:
        model = OpetationLog
        exclude = ()