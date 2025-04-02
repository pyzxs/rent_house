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
    Public ORM model, base table
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Primary key ID')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), comment='Creation time')
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        comment='Update time'
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment='Deletion time')

    @classmethod
    def get_column_attrs(cls) -> list:
        """
        Get all field names in the model except relationships
        :return: list of column attributes
        """
        mapper = inspect(cls)
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
