#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/18 22:19
# @File           : user.py
# @IDE            : PyCharm
# @desc           : Query parameters - class dependencies

"""
Class dependencies - Official documentation: https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from typing import Union

from fastapi import Depends, Query

from core.dependencies import Paging, QueryParams


class UserParams(QueryParams):
    """
    List pagination
    """

    def __init__(
            self,
            name: Union[str, None] = Query(None, description="User name"),
            telephone: Union[str, None] = Query(None, description="Phone number"),
            disabled: Union[bool, None] = Query(None, description="Whether disabled"),
            is_staff: Union[bool, None] = Query(None, description="Whether staff"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.telephone = ("like", telephone)
        self.disabled = disabled
        self.is_staff = is_staff


class RoleParams(QueryParams):
    """
    List pagination
    """

    def __init__(
            self,
            name: Union[str, None] = Query(None, description="Role name"),
            role_key: Union[str, None] = Query(None, description="Permission key"),
            disabled: Union[bool, None] = Query(None, description="Whether disabled"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.role_key = ("like", role_key)
        self.disabled = disabled

