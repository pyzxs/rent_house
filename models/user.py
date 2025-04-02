# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : user.py
# @desc           : 主配置文件
from datetime import datetime
from typing import Union, Optional

from sqlalchemy import String, Boolean, Column, Integer, ForeignKey, Table, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from passlib.context import CryptContext

from core.base import BaseModel
from core.database import Base

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
    comment="user has many roles"
)

role_menus = Table(
    "role_menus",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
    Column("menu_id", Integer, ForeignKey("menus.id", ondelete="CASCADE")),
    comment="role has many menus"
)


class Menu(BaseModel):
    __tablename__ = "menus"
    __table_args__ = ({'comment': 'menus table'})

    title: Mapped[str] = mapped_column(String(50), comment="菜单标题")
    name: Mapped[str] = mapped_column(String(50), comment="菜单名称")
    icon: Mapped[Union[str, None]] = mapped_column(String(50), comment="菜单图标")
    redirect: Mapped[Union[str, None]] = mapped_column(String(100), comment="重定向地址")
    component: Mapped[Union[str, None]] = mapped_column(String(255), comment="前端组件地址")
    path: Mapped[Union[str, None]] = mapped_column(String(50), comment="前端路由地址")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    hidden: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否隐藏")
    menu_type: Mapped[int] = mapped_column(Integer, default=0, comment="菜单类型：0、目录 1、菜单 2、按钮")
    perms: Mapped[Optional[str]] = mapped_column(String(50), comment="权限标识", unique=False, index=True)
    order: Mapped[int] = mapped_column(Integer, comment="排序")

    """以下属性主要用于补全前端路由属性，"""
    no_cache: Mapped[bool] = mapped_column(
        Boolean,
        comment="如果设置为true，则不会被 <keep-alive> 缓存(默认 false)",
        default=False
    )
    affix: Mapped[bool] = mapped_column(
        Boolean,
        comment="如果设置为true，则会一直固定在tag项中(默认 false)",
        default=False
    )
    parent_id: Mapped[Union[int, None]] = mapped_column(
        Integer,
        ForeignKey("menus.id"),
        nullable=True,
        comment="parent menu id"
    )

    @staticmethod
    def menus_order(datas: list, order: str = "order", children: str = "children") -> list:
        """
        菜单排序
        :param datas:
        :param order:
        :param children:
        :return:
        """
        result = sorted(datas, key=lambda menu: menu[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda menu: menu[order])
        return result


class Role(BaseModel):
    __tablename__ = "roles"
    __table_args__ = ({'comment': '角色表'})
    role_key: Mapped[str] = mapped_column(String(50), index=True, comment="角色key")
    name: Mapped[str] = mapped_column(String(50), index=True, comment="名称")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    order: Mapped[int or None] = mapped_column(Integer, default=0, comment="排序")
    desc: Mapped[str or None] = mapped_column(String(255), nullable=True, comment="描述")
    is_admin: Mapped[bool] = mapped_column(Boolean, comment="是否为超级角色", default=False)

    menus: Mapped[set[Menu]] = relationship(secondary=role_menus)


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = ({'comment': '用户表'})
    telephone: Mapped[str] = mapped_column(String(11), index=True, unique=True, comment="手机号码")
    password: Mapped[str] = mapped_column(String(128), comment="密码")
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="姓名")
    nickname: Mapped[str or None] = mapped_column(String(50), nullable=True, comment="昵称")
    gender: Mapped[str or None] = mapped_column(String(8), nullable=True, comment="性别")
    disabled: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否禁用")
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否为工作人员")
    last_ip: Mapped[str or None] = mapped_column(String(50), nullable=True, comment="最后一次登录IP")
    last_login_at: Mapped[datetime or None] = mapped_column(DateTime, nullable=True, comment="最近一次登录时间")

    roles: Mapped[set[Role]] = relationship(secondary=user_roles)
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        生成哈希密码
        :param password: 原始密码
        :return: 哈希密码
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        验证原始密码是否与哈希密码一致
        :param password: 原始密码
        :param hashed_password: 哈希密码
        :return:
        """
        return pwd_context.verify(password, hashed_password)

    @property
    def is_admin(self) -> bool:
        """
        获取该用户是否拥有最高权限
        以最高权限为准
        :return:
        """
        return any([i.is_admin for i in self.roles])
