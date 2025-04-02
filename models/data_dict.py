# -*- coding: UTF-8 -*-
# @Project ：Apartment-partner-server 
# @version : 1.0
# @File    ：data_dict.py
# @Author  ：ben
# @Date    ：2025/3/6 上午9:53 
# @desc    : 数据字典
from typing import Union

from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.base import BaseModel


class DictType(BaseModel):
    __tablename__ = "dict_type"
    __table_args__ = ({'comment': '字典类型表'})
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="字典名称")
    tp: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="字典类型")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="字典状态，是否禁用")
    remark: Mapped[Union[str, None]] = mapped_column(String(255), nullable=True, comment="备注")
    details: Mapped[list["DictDetails"]] = relationship(back_populates="dict_type")


class DictDetails(BaseModel):
    __tablename__ = "dict_details"
    __table_args__ = ({'comment': '字典详情表'})

    label: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="字典标签")
    value: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="字典键值")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="字典状态，是否禁用")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否默认")
    order: Mapped[int] = mapped_column(Integer, comment="字典排序")
    dict_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dict_type.id", ondelete='CASCADE'),
        comment="关联字典类型"
    )
    dict_type: Mapped[DictType] = relationship(foreign_keys=dict_type_id, back_populates="details")
    remark: Mapped[Union[str,None]] = mapped_column(String(255), nullable=True, comment="备注")
