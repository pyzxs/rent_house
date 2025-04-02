# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：helpers.py.py
# @Author  ：ben
# @Date    ：2025/4/2 13:36 
# @desc    : utility functions

import random
import re
import string
from typing import List, Union, Any, Callable


def valid_password(password: str) -> Union[str, bool]:
    """
    Check password strength
    """
    if len(password) < 8 or len(password) > 16:
        return 'Password length must be between 8-16 characters'
    else:
        for i in password:
            if 0x4e00 <= ord(i) <= 0x9fa5 or ord(i) == 0x20:  # 0x4e00 and other hex values are Unicode for Chinese characters and space
                return 'Spaces and Chinese characters are not allowed'
        else:
            key = 0
            key += 1 if bool(re.search(r'\d', password)) else 0
            key += 1 if bool(re.search(r'[A-Za-z]', password)) else 0
            key += 1 if bool(re.search(r"\W", password)) else 0
            if key >= 2:
                return True
            else:
                return 'Must contain at least 2 combinations of numbers/letters/special characters'


def generate_string(length: int = 8) -> str:
    """
    Generate random string
    :param length: string length
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def date2str(dt, f="%Y-%m-%d %H:%M:%S") -> str:
    if isinstance(dt, str):
        return dt
    return dt.strftime(f)


def model_validate_out(obj, schemas) -> dict[str, Any]:
    """
    Map SQLAlchemy object to Pydantic model
    :param obj : SQLAlchemy object
    :param schemas : Pydantic model
    :return: validated dictionary
    """
    return schemas.model_validate(obj).model_dump()


def list_dict_find(options: List[dict], key: str, value: any) -> Union[dict, None]:
    """
    Find item in list of dictionaries
    """
    return next((item for item in options if item.get(key) == value), None)


def dict_to_list_by_key(options: List[dict], key: str) -> list:
    """
    Generate new list based on specific key in dictionaries
    :param options: list of dictionaries
    :param key: key to extract
    :return: list of values
    """
    return list(map(lambda item: item[key], options))

