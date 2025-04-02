# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : response.py
# @desc           : 主配置文件
from typing import Union

from fastapi.responses import ORJSONResponse as Response
from fastapi import status


class SuccessResponse(Response):
    """
    成功响应
    """

    def __init__(self, data=None, message="success", code=status.HTTP_200_OK, **kwargs):
        self.data = {
            "code": code,
            "message": message,
            "data": data
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=code)


class ErrorResponse(Response):
    """
    失败响应
    """

    def __init__(self, message=None, code=status.HTTP_400_BAD_REQUEST, **kwargs):
        self.data = {
            "code": code,
            "message": message,
            "data": []
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=code)
