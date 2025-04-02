# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：helpers.py.py
# @Author  ：ben
# @Date    ：2025/4/2 下午1:36 
# @desc    : function tools

import random
import re
import string
from typing import List, Union, Any, Callable


def valid_password(password: str) -> Union[str, bool]:
    """
    检测密码强度
    """
    if len(password) < 8 or len(password) > 16:
        return '长度需为8-16个字符,请重新输入。'
    else:
        for i in password:
            if 0x4e00 <= ord(i) <= 0x9fa5 or ord(i) == 0x20:  # Ox4e00等十六进制数分别为中文字符和空格的Unicode编码
                return '不能使用空格、中文，请重新输入。'
        else:
            key = 0
            key += 1 if bool(re.search(r'\d', password)) else 0
            key += 1 if bool(re.search(r'[A-Za-z]', password)) else 0
            key += 1 if bool(re.search(r"\W", password)) else 0
            if key >= 2:
                return True
            else:
                return '至少含数字/字母/字符2种组合，请重新输入。'


def generate_string(length: int = 8) -> str:
    """
    生成随机字符串
    :param length: 字符串长度
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def date2str(dt, f="%Y-%m-%d %H:%M:%S") -> str:
    if isinstance(dt, str):
        return dt
    return dt.strftime(f)


def model_validate_out(obj, schemas) -> dict[str, Any]:
    """
    映射sqlalchemy对象到dydantic模型
    :param obj : sqlalchemy对象:
    :param schemas : pydantic模型:
    :return:
    """
    return schemas.model_validate(obj).model_dump()


def list_dict_find(options: List[dict], key: str, value: any) -> Union[dict, None]:
    """
    字典列表查找
    """
    return next((item for item in options if item.get(key) == value), None)


def dict_to_list_by_key(options: List[dict], key: str) -> list:
    """
    已字典中某个键重新生成列表
    :param options:
    :param key:
    :return:
    """
    return list(map(lambda item: item[key], options))

