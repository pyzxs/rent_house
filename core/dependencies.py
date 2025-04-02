# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : dependencies.py.py
# @desc           : 注入接口参数依赖


import copy

from fastapi import Body


class QueryParams:

    def __init__(self, params=None):
        if params:
            self.page = params.page
            self.limit = params.limit
            self.offset = (self.page - 1) * self.limit
            self.v_order = params.v_order
            self.v_order_field = params.v_order_field

    def dict(self, exclude: list[str] = None) -> dict:
        result = copy.deepcopy(self.__dict__)
        if exclude:
            for item in exclude:
                try:
                    del result[item]
                except KeyError:
                    pass
        return result

    def to_where(self, exclude: list[str] = None) -> dict:
        params = self.dict(exclude=exclude)
        del params["page"]
        del params["limit"]
        del params["v_order"]
        del params["v_order_field"]
        del params["offset"]
        return params


class Paging(QueryParams):
    """
    列表分页
    """

    def __init__(self, page: int = 1, limit: int = 10, v_order_field: str = None, v_order: str = None):
        super().__init__()
        self.page = page
        self.limit = limit
        self.offset = (self.page - 1) * self.limit
        self.v_order = v_order
        self.v_order_field = v_order_field


class IdList:
    """
    id 列表
    """

    def __init__(self, ids: list[int] = Body(..., title="ID 列表")):
        self.ids = ids
