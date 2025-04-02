# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：request_schemas.py.py
# @Author  ：ben
# @Date    ：2025/4/2 下午5:28 
# @desc    : request schemas
from pydantic import BaseModel, Field


class LoginUser(BaseModel):
    username: str = Field(..., description="login user")
    password: str = Field(..., min_length=3, max_length=50)
    platform: str = Field(default='0', description="platform: 0、PC admin platform 1、front app")
    method: str = Field(default='0', description="method： 0、telephone")


class Token(BaseModel):
    access_token: str = Field(..., description='login Token')
    token_type: str = Field(..., description="jwt token_type")
