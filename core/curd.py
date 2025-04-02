# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : curd.py
# @desc           : CRUD operations

from typing import Any, Optional, Union
from sqlalchemy import and_, or_, not_, func
from sqlalchemy.orm import Query

def get_filter_where(model, **kwargs) -> list:
    """
    Generate filter conditions based on model fields
    :param model: SQLAlchemy model
    :param kwargs: filter conditions
    :return: list of filter conditions
    """
    conditions = []
    for key, value in kwargs.items():
        if value is not None and hasattr(model, key):
            if isinstance(value, (list, tuple)):
                conditions.append(getattr(model, key).in_(value))
            else:
                conditions.append(getattr(model, key) == value)
    return conditions

def order_by(query: Query, model, params: dict) -> Query:
    """
    Add order by clause to query
    :param query: SQLAlchemy query
    :param model: SQLAlchemy model
    :param params: order parameters
    :return: ordered query
    """
    if params.get('order_by') and hasattr(model, params['order_by']):
        order_field = getattr(model, params['order_by'])
        if params.get('order_type') == 'desc':
            query = query.order_by(order_field.desc())
        else:
            query = query.order_by(order_field.asc())
    return query

def paginate(query: Query, page: int = 1, page_size: int = 10) -> Query:
    """
    Add pagination to query
    :param query: SQLAlchemy query
    :param page: current page number
    :param page_size: number of items per page
    :return: paginated query
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    return query.offset((page - 1) * page_size).limit(page_size)

def get_count(query: Query) -> int:
    """
    Get total count of query results
    :param query: SQLAlchemy query
    :return: total count
    """
    return query.with_entities(func.count()).scalar()
