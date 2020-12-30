# -*- encoding: utf-8 -*-
"""
@File    : auth.py
@Time    : 2020/12/30 14:30
@Author  : wuhao
"""


import time

import jwt
from jwt import ExpiredSignatureError, DecodeError, InvalidTokenError
from jwt.exceptions import InvalidKeyError

from django.conf import settings

# config = getattr(settings, 'JWT_CONFIG')
from WTS.drf_settings import JWT_CONFIG

config = JWT_CONFIG

def parse_token(token):
    try:
        payload = jwt.decode(
            token, config['access_token_secret'],
            algorithms=config['jwt_header']['alg'],
            leeway=config['access_token_leeway']
        )
    except ExpiredSignatureError: # 声明过期触发
        return
    except (InvalidKeyError, DecodeError) as ex: #　密钥格式不正确时引发
        print(ex)
        return
    except InvalidTokenError as e: # 令牌失败时的基本异常
        print(e)
        return
    return payload


def create_token(user_id, expires=config['access_token_expires']):
    ts = time.time()
    payload = create_payload(
        user_id,
        ts + expires,
    )
    token = jwt.encode(
        payload, config['access_token_secret'],
        config['jwt_header']['alg'], config['jwt_header']
    ).decode('utf8')
    return dict(tk=token, expAt=ts + expires, uId=user_id)

def create_payload(uId, exp, **kwargs):
    return dict(uId=uId, exp=exp, **kwargs)


if __name__ == "__main__":

    create_token(1)