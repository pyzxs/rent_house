# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : auth.py
# @desc           : 授权管理
from datetime import timedelta, datetime
from typing import Optional, List, Union

import jwt
from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session

from config import settings
from config.settings import oauth2_scheme
from core.database import get_db
from core.exception import CustomException
from core.response import SuccessResponse, ErrorResponse
from models.user import User
from utils import helpers


def check_user_login(db, data):
    """
    fastapi授权登录
    :param db:
    :param data:
    :return:
    """
    user = get_user_by_telephone(db, data.username)
    error_code = status.HTTP_401_UNAUTHORIZED
    if not user:
        raise CustomException(status_code=error_code, code=error_code, msg="该手机号不存在")

    result = User.verify_password(data.password, user.password)
    if not result:
        raise CustomException(status_code=error_code, code=error_code, msg="手机号或密码错误")
    if user.disabled:
        raise CustomException(status_code=error_code, code=error_code, msg="此手机号已被冻结")
    data = {"id": user.id, "telephone": user.telephone}
    expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(data, expire)


def create_token(payload: dict, expires: timedelta = None):
    """
    创建一个生成新的访问令牌的工具函数。

    pyjwt：https://github.com/jpadilla/pyjwt/blob/master/docs/usage.rst
    jwt 博客：https://geek-docs.com/python/python-tutorial/j_python-jwt.html

    #TODO 传入的时间为UTC时间datetime.datetime类型，但是在解码时获取到的是本机时间的时间戳
    """
    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        uid: str = payload.get("id")
        if uid is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.query(User).get(uid)

    if user is None:
        raise credentials_exception
    return user


def get_current_permission_user(required_perms: Optional[List[str]] = None):
    """
    获取当前用户并验证权限的依赖函数
    :param required_perms: 需要验证的权限列表
    :return: 返回一个依赖函数
    """

    async def current_user_with_perms(
            user: User = Depends(get_current_user)
    ) -> User:
        check_user_permissions(required_perms, user)
        return user

    return current_user_with_perms


def check_user_permissions(perms: Optional[List[str]], user: User):
    """
    验证接口是否有权限
    :param perms:
    :param user:
    :return:
    """
    check_perms = set(perms) if perms else None
    user_perms = get_user_permissions(user)
    ALL_PERMISSIONS = {'*.*.*'}
    # 当存在需要检查的权限且用户不具有全权限时，进行权限校验
    if check_perms and ALL_PERMISSIONS.isdisjoint(user_perms):
        # 使用 isdisjoint 方法比集合交集更高效
        if user_perms.isdisjoint(check_perms):
            raise CustomException(
                msg="无权限操作",
                code=status.HTTP_403_FORBIDDEN
            )


def get_user_permissions(user: User):
    """
    获取用户权限
    :param user:
    :return:
    """
    if user.is_admin:
        return {'*.*.*'}

    permissions = set()
    for role_obj in user.roles:
        for menu in role_obj.menus:
            if menu.perms and not menu.disabled:
                permissions.add(menu.perms)
    return permissions


async def check_telephone_login(db, request, form_data):
    """
    手机号码登录
    :param request:
    :param db:
    :param form_data:
    :return:
    """
    user = get_user_by_telephone(db, form_data.username)
    try:
        # 手机账号密码登录
        if form_data.platform not in ["0", "1"]:
            raise ValueError("赞不支持其它平台")
        if form_data.method != '0':
            raise ValueError("暂不支持其它登陆方式")
        if not user:
            raise ValueError("该手机用户不存在")
        if not User.verify_password(form_data.password, user.password):
            raise ValueError("用户输入密码错误")
        if form_data.platform == '0' and not user.is_staff:
            raise ValueError("登录管理后台必须是平台员工")

    except ValueError as e:
        return ErrorResponse(str(e))

    return await check_normal_user_login(db, user, request)


async def check_normal_user_login(db, user, request):
    """
    通用验证设置
    :param db:
    :param request:
    :param user:
    :return:
    """
    try:
        if not user:
            raise ValueError("手机号不存在")
        elif user.disabled:
            raise ValueError("手机号已被冻结")
    except ValueError as e:
        return ErrorResponse(str(e))

        # 登录成功创建 token
    data = {"id": user.id, "telephone": user.telephone}
    access_token = create_token(data)

    result = {
        "id": user.id,
        "access_token": access_token,
        "name": user.name,
        "telephone": user.telephone,
        "is_staff": user.is_staff,  # 是否为员工
        "is_admin": user.is_admin,  # 是否为管理员
    }
    await update_login_info(db, user, request.client.host)
    return SuccessResponse(result, "登录成功")


async def update_login_info(db, user, last_ip: str) -> None:
    """
    更新当前登录信息
    :param db:
    :param user: 用户对象
    :param last_ip: 最近一次登录 IP
    :return:
    """
    user.last_ip = last_ip
    user.last_login_at = datetime.now()
    db.flush()


async def reset_user_current_password(db, u, form_data):
    """
    重置当前用户用户密码
    :param db:
    :param u:
    :param form_data:
    :return:
    """
    if form_data.password != form_data.password_two:
        raise CustomException(msg="两次密码不一致", code=400)

    result = helpers.valid_password(form_data.password)
    if isinstance(result, str):
        raise CustomException(result)

    u.password = User.get_password_hash(form_data.password)
    db.flush(u)


def get_user_by_telephone(db: Session, telephone: str) -> Union[User, None]:
    """通过手机号获取用户对象"""
    return db.query(User).filter(User.telephone == telephone).first()
