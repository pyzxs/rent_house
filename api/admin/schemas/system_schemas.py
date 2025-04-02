# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : request_schemas.py
# @desc           : 请求数据
from typing import Union, List, Optional

from pydantic import BaseModel, Field, ConfigDict

from core.datatype import Telephone


class User(BaseModel):
    telephone: Telephone = Field(..., description="手机号码")
    name: str = Field(default='', min_length=2, max_length=50)
    avatar: Union[str, None] = Field(default=None, description="用户头像")
    nickname: Union[str, None] = Field(default='', min_length=2, max_length=50)
    disabled: bool = Field(default=False, description="是否禁止")
    gender: Union[str, None] = Field(default='0', description="性别")
    is_staff: bool = Field(default=False, description="是否是员工")


class UserRequest(User):
    role_ids: list[int] = []
    password: Union[str, None] = Field(default=None)


class UserResponse(User):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="用户ID")


class Menu(BaseModel):
    title: str = Field(..., description="菜单标题")
    name: str = Field(..., description="菜单名称")
    icon: Union[str, None] = Field(default='', description="菜单图标")
    redirect: Union[str, None] = Field(None, description="重定向地址")
    component: Union[str, None] = Field(description="前端组件地址")
    path: Union[str, None] = Field(description="前端路由地址")
    disabled: bool = Field(default=False, description="是否禁用")
    hidden: bool = Field(default=False, description="是否隐藏")
    order: int = Field(default=0, description="排序")
    menu_type: int = Field(default=0, description="菜单类型： 0、目录 1、菜单 2、按钮")
    perms: Optional[str] = Field(None, description="权限标识")
    parent_id: Union[int, None] = Field(default=0, description="父级ID")
    no_cache: Union[bool, None] = Field(default=False, description="是否缓存")
    affix: Union[bool, None] = Field(default=False, description="禁锢导航栏")


class Meta(BaseModel):
    title: str
    icon: Union[str, None] = None
    keepAlive: Union[bool, None] = False
    hideInMenu: Union[bool, None] = False
    affixTab: Union[bool, None] = False
    order: Union[int, None] = None


class RouterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="菜单Id")
    name: Union[str, None] = None
    component: Union[str, None] = None
    path: str
    redirect: Union[str, None] = None
    meta: Union[Meta, None] = None
    index: Union[int, None] = None
    children: list[dict] = []


class MenuTreeResponse(Menu):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="菜单Id")
    children: Union[list[dict], None] = None


class Role(BaseModel):
    role_key: str = Field(..., description="角色key")
    name: str = Field(..., description="角色名称")
    data_range: int = Field(default=0, description="角色数据权限，预留")
    disabled: bool = Field(default=False, description="是否禁止")
    order: int = Field(default=0, description="排序")
    desc: str = Field(description="描述")


class RoleRequest(Role):
    menu_ids: Union[list[int], None] = []


class DictTypeRequest(BaseModel):
    name: str
    tp: str
    disabled: bool
    remark: str


class DictDetailRequest(BaseModel):
    label: str
    value: str
    disabled: bool
    is_default: bool
    order: int = None
    remark: str = None
