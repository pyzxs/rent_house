# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：views.py
# @Author  ：ben
# @Date    ：2025/4/2 下午5:27 
# @desc    : 注释内容
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from starlette.requests import Request

from api.index.schemas import request_schemas
from core.database import get_db, get_cache, get_async_db
from services import auth

indexAPI = APIRouter()


@indexAPI.post("/login", response_model=request_schemas.Token, name="文档登录认证", include_in_schema=False)
async def api_login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = auth.check_user_login(db, data)
    return {"access_token": token, "token_type": "bearer"}


@indexAPI.post("/user/login", summary="用户登录系统")
async def user_login(request: Request, form_data: request_schemas.LoginUser, db: Session = Depends(get_db)):
    return await auth.check_telephone_login(db, request, form_data)