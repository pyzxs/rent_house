# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : base.py
# @desc           : ORM Base

from datetime import datetime

from sqlalchemy import DateTime, Integer, func, inspect
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class BaseModel(Base):
    """
    public  ORM model，base table
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键ID')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment='创建时间')
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        comment='update time'
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment='删除时间')

    @classmethod
    def get_column_attrs(cls) -> list:
        """
        获取模型中除 relationships 外的所有字段名称
        :return:
        """
        mapper = inspect(cls)

        # for attr_name, column_property in mapper.column_attrs.items():
        #     # single column property
        #     column = column_property.columns[0]
        #     # all property
        #     print(f"attr: {attr_name}")
        #     print(f"type: {column.type}")
        #     print(f"default: {column.default}")
        #     print(f"server default: {column.server_default}")

        return mapper.column_attrs.keys()

    @classmethod
    def get_attrs(cls) -> list:
        """
        get model all fields attributes
        :return:
        """
        mapper = inspect(cls)
        return mapper.attrs.keys()

    @classmethod
    def get_relationships_attrs(cls) -> list:
        """
        model relationships all fields attributes
        :return:
        """
        mapper = inspect(cls)
        return mapper.relationships.keys()
