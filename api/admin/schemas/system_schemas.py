# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : request_schemas.py
# @desc           : Request data schemas
from typing import Union, Optional

from pydantic import BaseModel, Field, ConfigDict

from core.datatype import Telephone, DatetimeStr


class User(BaseModel):
    telephone: Telephone = Field(..., description="Phone number")
    name: str = Field(default='', min_length=2, max_length=50)
    nickname: Union[str, None] = Field(default='', min_length=2, max_length=50)
    disabled: bool = Field(default=False, description="Whether disabled")
    gender: Union[str, None] = Field(default='0', description="Gender")
    is_staff: bool = Field(default=False, description="Whether staff")


class UserRequest(User):
    role_ids: list[int] = []
    dept_ids: list[int] = []
    password: Union[str, None] = Field(default=None)


class UserResponse(User):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="User ID")


class Menu(BaseModel):
    title: str = Field(..., description="Menu title")
    name: str = Field(..., description="Menu name")
    icon: Union[str, None] = Field(default='', description="Menu icon")
    redirect: Union[str, None] = Field(None, description="Redirect address")
    component: Union[str, None] = Field(description="Frontend component path")
    path: Union[str, None] = Field(description="Frontend route path")
    disabled: bool = Field(default=False, description="Whether disabled")
    hidden: bool = Field(default=False, description="Whether hidden")
    order: int = Field(default=0, description="Sort order")
    menu_type: int = Field(default=0, description="Menu type: 0=directory, 1=menu, 2=button")
    perms: Optional[str] = Field(None, description="Permission identifier")
    parent_id: Union[int, None] = Field(default=0, description="Parent ID")
    no_cache: Union[bool, None] = Field(default=False, description="Whether to cache")
    affix: Union[bool, None] = Field(default=False, description="Pin to navigation bar")


class Meta(BaseModel):
    title: str
    icon: Union[str, None] = None
    keepAlive: Union[bool, None] = False
    hideInMenu: Union[bool, None] = False
    affixTab: Union[bool, None] = False
    order: Union[int, None] = None


class RouterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Menu ID")
    name: Union[str, None] = None
    component: Union[str, None] = None
    path: str
    redirect: Union[str, None] = None
    meta: Union[Meta, None] = None
    index: Union[int, None] = None
    children: list[dict] = []


class MenuTreeResponse(Menu):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(..., description="Menu ID")
    children: Union[list[dict], None] = None


class Role(BaseModel):
    role_key: str = Field(..., description="Role key")
    name: str = Field(..., description="Role name")
    data_range: int = Field(default=0, description="Role data scope (reserved)")
    disabled: bool = Field(default=False, description="Whether disabled")
    order: int = Field(default=0, description="Sort order")
    desc: str = Field(default='',description="Description")
    is_admin: bool = Field(default=False, description="is super admin")


class RoleRequest(Role):
    menu_ids: Union[list[int], None] = []
    dept_ids: list[int] = []


class Department(BaseModel):
    name: str
    dept_key: str
    disabled: bool = False
    order: int | None = None
    desc: str | None = None
    owner: str | None = None
    phone: str | None = None
    email: str | None = None
    parent_id: int | None = None


class DepartmentResponse(Department):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: DatetimeStr
    updated_at: DatetimeStr


class DeptTreeListOut(DepartmentResponse):
    model_config = ConfigDict(from_attributes=True)
    children: list[dict] = []


class DictTypeRequest(BaseModel):
    name: str = Field(..., description="Dictionary type name")
    tp: str = Field(description="Dictionary type")
    disabled: bool = Field(default=False, description="Whether disabled")
    remark: str = Field(description="Remark")


class DictDetailRequest(BaseModel):
    label: str = Field(description="Label name")
    value: str = Field(description="Label value")
    disabled: bool = Field(default=False, description="Whether disabled")
    is_default: bool = Field(default=False, description="Whether default")
    order: int = Field(default=0, description="Sort order")
    remark: str = Field(default='', description="Remark")
