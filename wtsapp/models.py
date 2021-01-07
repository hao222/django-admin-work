from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.db.models import CharField, IntegerField, ForeignKey, CASCADE, DateTimeField

from v1.models_helper.enums import StatusEnum, WStatusEnum, TStatusEnum

phone_validator = RegexValidator(r"^1[3456789][0-9]{9}$", "请输入正确的手机号码。")


class BaseModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    modify_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True

class Role(BaseModel):
    name = CharField(
        max_length=64, verbose_name='角色名', help_text='角色名，最多64个字符',
        name='name', unique=True)
    status = IntegerField(
        choices=StatusEnum.choices(), default=StatusEnum.default(),
        verbose_name='状态', name='status')

    def __str__(self):
        return f'角色名为: {self.name}'


class User(AbstractUser, BaseModel):
    """
    用户信息
    """
    phone = CharField(max_length=11, default=None, null=True, db_index=True, validators=[phone_validator])
    status = IntegerField(
        choices=StatusEnum.choices(), default=StatusEnum.default(),
        verbose_name='状态', name='status')
    role = ForeignKey(
        Role, verbose_name='角色', db_column='role_id', on_delete=CASCADE,
        help_text='角色', name='role', null=True, default=None)

    def __str__(self):
        return f'用户为: {self.username}'

class TaskPro(BaseModel):
    """ 任务 """
    user = ForeignKey(
        User, verbose_name='用户', db_column='user_id', on_delete=CASCADE,
        help_text='用户', name='user', null=True, related_name="tasks")
    task_name = CharField(
        max_length=64, verbose_name='任务名', help_text='任务，最多64个字符',
        name='task_name')
    start_at = DateTimeField(
        verbose_name='任务开始时间', help_text='任务开始时间', null=True,
        default=None, name='start_at')
    end_at = DateTimeField(
        verbose_name='任务终止时间', help_text='任务终止时间', null=True,
        default=None, name='end_at')

    task_status = IntegerField(
        choices=TStatusEnum.choices(), default=TStatusEnum.default(),
        verbose_name='任务状态', name='task_status')
    parent = ForeignKey('self', null=True, default=None, on_delete=models.CASCADE, related_name='children', blank=True, name='parent', db_column="parent_id")
    creator = CharField(max_length=32, default="", null=True, blank=True, verbose_name="任务创建者")
    task_process = CharField(
        max_length=2, verbose_name='任务进度', help_text='任务进度，0-100', default="0",
        name='task_process')
    task_info = CharField(max_length=1024, default="", verbose_name="任务内容", name="task_info")
    # @property
    # def task_process(self):
    #     """
    #     任务进度
    #     :return:
    #     """
    #     childrens = self.children.count()
    #     success_chids = self.children.filter( task_status=2).count()
    #     percent = success_chids / childrens
    #     return f"{percent:.2%}"

    def __str__(self):
        return f"任务名: {self.task_name}"


class Working(BaseModel):
    """ 工时 """
    taskpro = ForeignKey(
        TaskPro, verbose_name='任务', on_delete=CASCADE,
        help_text='任务', null=True, related_name="works")
    work_start = DateTimeField(
        verbose_name='工时开始日期', help_text='工时开始日期', null=True,
        default=None, name='work_start')
    work_end = DateTimeField(
        verbose_name='工时终止日期', help_text='工时终止日期', null=True,
        default=None, name='work_end')
    approve_status = IntegerField(
        choices=WStatusEnum.choices(), default=WStatusEnum.default(),
        verbose_name='审批状态', name='approve_status')
    approve_time = DateTimeField(help_text="审批通过时间", default=None, blank=True, null=True)
    reasons = CharField(max_length=32, default="", blank=True, null=True, help_text="建议")
    work_info = CharField(max_length=1024, default="", blank=True, null=True, help_text="工时内容")
    work_time = CharField(max_length=32, default="0", help_text="工作时长", null=True, blank=True)
    approveor = CharField(max_length=32, default="", help_text="审批人", null=True, blank=True)

    def __str__(self):
        return f"工时父类: {self.taskpro.task_name}"

class OpetationLog(BaseModel):
    """ 操作日志 """
    operator = ForeignKey(
        User, verbose_name='操作人', on_delete=CASCADE, help_text='操作人',
        name='operator', null=True)
    module = CharField(
        max_length=32, verbose_name='功能模块', help_text='功能模块',
        name='module')
    operation = CharField(
        max_length=32, verbose_name='操作内容', help_text='操作内容',
        name='operation')
    operation_name = CharField(
        max_length=32, verbose_name='修改人', help_text='修改人',
        name='operation_name', blank=True, null=True, default="")


class AuthUser:
    """ 模拟返回request.user """
    def __init__(self, instance, info):
        self.instance = instance
        self.info = info
        self.is_authenticated = True