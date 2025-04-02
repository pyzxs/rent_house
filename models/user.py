# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : user.py
# @desc           : Main configuration file
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
    comment="User can have multiple roles"
)

role_menus = Table(
    "role_menus",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
    Column("menu_id", Integer, ForeignKey("menus.id", ondelete="CASCADE")),
    comment="role has many menus"
)

user_departments = Table(
    "user_departments",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("dept_id", Integer, ForeignKey("departments.id", ondelete="CASCADE")),
)

role_departments = Table(
    "role_departments",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE")),
    Column("dept_id", Integer, ForeignKey("departments.id", ondelete="CASCADE")),
)


class Menu(BaseModel):
    __tablename__ = "menus"
    __table_args__ = ({'comment': 'Menus table'})

    title: Mapped[str] = mapped_column(String(50), comment="Menu title")
    name: Mapped[str] = mapped_column(String(50), comment="Menu name")
    icon: Mapped[Union[str, None]] = mapped_column(String(50), comment="Menu icon")
    redirect: Mapped[Union[str, None]] = mapped_column(String(100), comment="Redirect address")
    component: Mapped[Union[str, None]] = mapped_column(String(255), comment="Frontend component path")
    path: Mapped[Union[str, None]] = mapped_column(String(50), comment="Frontend route path")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="Whether disabled")
    hidden: Mapped[bool] = mapped_column(Boolean, default=False, comment="Whether hidden")
    menu_type: Mapped[int] = mapped_column(Integer, default=0, comment="Menu type: 0=directory, 1=menu, 2=button")
    perms: Mapped[Optional[str]] = mapped_column(String(50), comment="Permission identifier", unique=False, index=True)
    order: Mapped[int] = mapped_column(Integer, comment="Sort order")

    no_cache: Mapped[bool] = mapped_column(
        Boolean,
        comment="If set to true, will not be cached by <keep-alive> (default false)",
        default=False
    )
    affix: Mapped[bool] = mapped_column(
        Boolean,
        comment="If set to true, will be fixed in tag items (default false)",
        default=False
    )

    @staticmethod
    def menus_order(datas: list, order: str = "order", children: str = "children") -> list:
        """
        Sort menus
        :param datas: menu data
        :param order: sort field
        :param children: children field
        :return: sorted menu list
        """
        result = sorted(datas, key=lambda menu: menu[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda menu: menu[order])
        return result


class Role(BaseModel):
    __tablename__ = "roles"
    __table_args__ = ({'comment': 'Roles table'})
    role_key: Mapped[str] = mapped_column(String(50), index=True, comment="Role key")
    name: Mapped[str] = mapped_column(String(50), index=True, comment="Name")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="Whether disabled")
    data_range: Mapped[int] = mapped_column(Integer, default=4, comment="Data permission scope")
    order: Mapped[int or None] = mapped_column(Integer, default=0, comment="Sort order")
    desc: Mapped[str or None] = mapped_column(String(255), nullable=True, comment="Description")
    is_admin: Mapped[bool] = mapped_column(Boolean, comment="Whether super role", default=False)

    menus: Mapped[set[Menu]] = relationship(secondary=role_menus)
    departments: Mapped[set["Department"]] = relationship(secondary=role_departments)


class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = ({'comment': 'Users table'})
    telephone: Mapped[str] = mapped_column(String(11), index=True, unique=True, comment="Phone number")
    password: Mapped[str] = mapped_column(String(128), comment="Password")
    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="Full name")
    nickname: Mapped[str or None] = mapped_column(String(50), nullable=True, comment="Nickname")
    gender: Mapped[str or None] = mapped_column(String(8), nullable=True, comment="Gender")
    disabled: Mapped[bool] = mapped_column(Boolean, default=True, comment="Whether disabled")
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False, comment="Whether staff member")
    last_ip: Mapped[str or None] = mapped_column(String(50), nullable=True, comment="Last login IP")
    last_login_at: Mapped[datetime or None] = mapped_column(DateTime, nullable=True, comment="Last login time")

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generate hashed password
        :param password: plain password
        :return: hashed password
        """

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify if plain password matches hashed password
        :param password: plain password
        :param hashed_password: hashed password
        :return: verification result
        """

    @property
    def is_admin(self) -> bool:
        """
        Check if user has super privileges
        :return: whether user has super privileges
        """
        return any([i.is_admin for i in self.roles])


class Department(BaseModel):
    __tablename__ = "departments"
    __table_args__ = ({'comment': 'Departments table'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="Department name")
    dept_key: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="Department key")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="Whether disabled")
    order: Mapped[int | None] = mapped_column(Integer, comment="Display order")
    desc: Mapped[str | None] = mapped_column(String(255), comment="Description")
    owner: Mapped[str | None] = mapped_column(String(255), comment="Manager")
    phone: Mapped[str | None] = mapped_column(String(255), comment="Contact phone")
    email: Mapped[str | None] = mapped_column(String(255), comment="Email")

    @classmethod
    def dept_order(cls, datas: list, order: str = "order", children: str = "children") -> list:
        """
        Sort departments
        :param datas: department data
        :param order: sort field
        :param children: children field
        :return: sorted department list
        """
        result = sorted(datas, key=lambda dept: dept[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda dept: dept[order])
        return result
