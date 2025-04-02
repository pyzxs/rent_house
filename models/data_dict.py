# -*- coding: UTF-8 -*-
# @Project ：Apartment-partner-server 
# @version : 1.0
# @File    ：data_dict.py
# @Author  ：ben
# @Date    ：2025/3/6 09:53 
# @desc    : Data dictionary
from typing import Union

from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.base import BaseModel


class DictType(BaseModel):
    __tablename__ = "dict_type"
    __table_args__ = ({'comment': 'Dictionary type table'})
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="Dictionary name")
    tp: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="Dictionary type")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="Dictionary status, whether disabled")
    remark: Mapped[Union[str, None]] = mapped_column(String(255), nullable=True, comment="Remark")
    details: Mapped[list["DictDetails"]] = relationship(back_populates="dict_type")


class DictDetails(BaseModel):
    __tablename__ = "dict_details"
    __table_args__ = ({'comment': 'Dictionary details table'})

    label: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="Dictionary label")
    value: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="Dictionary key value")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="Dictionary status, whether disabled")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, comment="Whether default")
    order: Mapped[int] = mapped_column(Integer, comment="Dictionary sort order")
    dict_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dict_type.id", ondelete='CASCADE'),
        comment="Associated dictionary type"
    )
    dict_type: Mapped[DictType] = relationship(foreign_keys=dict_type_id, back_populates="details")
    remark: Mapped[Union[str,None]] = mapped_column(String(255), nullable=True, comment="Remark")
