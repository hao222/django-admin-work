# -*- encoding: utf-8 -*-
"""
@File    : enums.py
@Time    : 2020/12/30 14:34
@Author  : wuhao
"""
from collections import OrderedDict
from enum import IntEnum, unique


class _ChoiceClass(IntEnum):

    @classmethod
    def choices(cls):
        return list(cls.__describe__.items())

    @classmethod
    def choice_dict(cls):
        return cls.__describe__

    @classmethod
    def describe_to_str(cls) -> str:
        return str(dict(cls.__describe__))

    @classmethod
    def get_display(cls, value) -> str:
        """ 获得对应的中文显示 """
        return cls.__describe__.get(int(value), '')


@unique
class GenderEnum(_ChoiceClass):
    male = 1
    female = 2
    __describe__ = dict(male=1, female=2)

    @classmethod
    def default(cls):
        return cls.male

@unique
class StatusEnum(_ChoiceClass):
    """
    状态
    """
    enabled = 1
    disabled = 0

    __describe__ = OrderedDict((
        (enabled, '启用'),
        (disabled, '禁用'),
    ))

    @classmethod
    def default(cls):
        return cls.enabled

@unique
class WStatusEnum(_ChoiceClass):
    """
    工时审批
    """
    pending = 0
    approve = 1
    not_pass = 2


    __describe__ = OrderedDict((
        (pending, '待审批'),
        (approve, '已审批'),
        (not_pass, '未通过'),
    ))

    @classmethod
    def default(cls):
        return cls.pending

@unique
class TStatusEnum(_ChoiceClass):
    """
    任务状态
    """
    non_begin = 0
    begin = 1
    success = 2
    cancel = 3
    close = 4

    __describe__ = OrderedDict((
        (non_begin, '未开始'),
        (begin, '进行中'),
        (success, '已完成'),
        (cancel, "已取消"),
        (close, "已关闭"),
    ))

    @classmethod
    def default(cls):
        return cls.non_begin


if __name__ == "__main__":
    print(GenderEnum(1))
