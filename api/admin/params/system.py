#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : user.py
# @IDE            : PyCharm
# @desc           : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from typing import Union

from fastapi import Depends, Query

from core.dependencies import Paging, QueryParams


class UserParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: Union[str, None] = Query(None, description="用户名称"),
            telephone: Union[str, None] = Query(None, description="手机号"),
            disabled: Union[bool, None] = Query(None, description="是否禁用"),
            is_staff: Union[bool, None] = Query(None, description="是否为工作人员"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.telephone = ("like", telephone)
        self.disabled = disabled
        self.is_staff = is_staff


class RoleParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: Union[str, None] = Query(None, description="角色名称"),
            role_key: Union[str, None] = Query(None, description="权限字符"),
            disabled: Union[bool, None] = Query(None, description="是否禁用"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.role_key = ("like", role_key)
        self.disabled = disabled

