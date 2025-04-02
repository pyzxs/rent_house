# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : datatype.py
# @desc           : 主配置文件


from typing import Annotated

from pydantic import AfterValidator, PlainSerializer, WithJsonSchema

from core.validator import *

# 实现自定义一个日期时间字符串的数据类型
DatetimeStr = Annotated[
    Union[str, datetime.datetime],
    AfterValidator(valid_datetime_or_str),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]

# 实现自定义一个手机号类型
Telephone = Annotated[
    str,
    AfterValidator(lambda x: valid_telephone(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]

# 实现自定义一个邮箱类型
Email = Annotated[
    str,
    AfterValidator(lambda x: valid_email(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]

# 实现自定义一个日期字符串的数据类型
DateStr = Annotated[
    Union[str, datetime.date],
    AfterValidator(valid_date_or_str),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]
