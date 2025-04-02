# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/14
# @File           : curd.py
# @desc           : 基础的curd操作
from datetime import datetime

from sqlalchemy import func

from core.exception import CustomException


def soft_delete(db, model, primary_id):
    """软删除"""
    db.query(model).filter_by(id=primary_id).update({"deleted_at": datetime.now()})
    db.commit()


def real_delete(db, model, primary_id):
    """真实删除"""
    db.query(model).filter_by(id=primary_id).delete()
    db.commit()


def get(db, model, primary_id):
    """获取详情"""
    return db.query(model).filter_by(id=primary_id).first()


def restore(db, row):
    """恢复软软删除"""
    row.deleted_at = None
    db.commit()


def order_by(query, model, page):
    """
    获取某模型的排序数据
    :param query:
    :param model:
    :param page:
    :return:
    """
    if page['v_order_field']:
        field = getattr(model, page['v_order_field'])
        if page['v_order'] == 'desc':
            query = query.order_by(field.desc())
        else:
            query = query.order_by(field.asc())
    return query


def get_filter_where(model, **kwargs):
    """
        字典过滤
        :param model:
        :param kwargs:
        """
    conditions = []
    for field, value in kwargs.items():
        if value is not None and value != "":
            attr = getattr(model, field)
            if isinstance(value, tuple):
                if len(value) == 1:
                    if value[0] == "None":
                        conditions.append(attr.is_(None))
                    elif value[0] == "not None":
                        conditions.append(attr.isnot(None))
                    else:
                        raise CustomException("SQL查询语法错误")
                elif len(value) == 2 and value[1] not in [None, [], ""]:
                    if value[0] == "date":
                        # 根据日期查询， 关键函数是：func.time_format和func.date_format
                        conditions.append(func.date_format(attr, "%Y-%m-%d") == value[1])
                    elif value[0] == "like":
                        conditions.append(attr.like(f"%{value[1]}%"))
                    elif value[0] == "in":
                        conditions.append(attr.in_(value[1]))
                    elif value[0] == "between" and len(value[1]) == 2:
                        conditions.append(attr.between(value[1][0], value[1][1]))
                    elif value[0] == "month":
                        conditions.append(func.date_format(attr, "%Y-%m") == value[1])
                    elif value[0] == "!=":
                        conditions.append(attr != value[1])
                    elif value[0] == ">":
                        conditions.append(attr > value[1])
                    elif value[0] == ">=":
                        conditions.append(attr >= value[1])
                    elif value[0] == "<=":
                        conditions.append(attr <= value[1])
                    else:
                        raise CustomException("SQL查询语法错误")
            else:
                conditions.append(attr == value)
    return conditions
