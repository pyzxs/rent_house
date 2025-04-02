# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : auth.py
# @desc           : Authorization management
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
    FastAPI authorization login
    :param db: database session
    :param data: login data
    :return: token
    """
    user = get_user_by_telephone(db, data.username)
    error_code = status.HTTP_401_UNAUTHORIZED
    if not user:
        raise CustomException(status_code=error_code, code=error_code, msg="Phone number does not exist")

    result = User.verify_password(data.password, user.password)
    if not result:
        raise CustomException(status_code=error_code, code=error_code, msg="Incorrect phone number or password")
    if user.disabled:
        raise CustomException(status_code=error_code, code=error_code, msg="This phone number has been frozen")
    data = {"id": user.id, "telephone": user.telephone}
    expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(data, expire)


def create_token(payload: dict, expires: timedelta = None):
    """
    Create a utility function to generate new access tokens.

    pyjwt: https://github.com/jpadilla/pyjwt/blob/master/docs/usage.rst
    jwt blog: https://geek-docs.com/python/python-tutorial/j_python-jwt.html

    #TODO The input time is UTC datetime type, but the decoded time is local timestamp
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
    Get current user and verify permissions dependency function
    :param required_perms: list of permissions to verify
    :return: dependency function
    """

    async def current_user_with_perms(
            user: User = Depends(get_current_user)
    ) -> User:
        check_user_permissions(required_perms, user)
        return user

    return current_user_with_perms


def check_user_permissions(perms: Optional[List[str]], user: User):
    """
    Verify if the interface has permission
    :param perms: permissions
    :param user: user object
    :return: None
    """
    check_perms = set(perms) if perms else None
    user_perms = get_user_permissions(user)
    ALL_PERMISSIONS = {'*.*.*'}
    # When there are permissions to check and the user does not have full permissions, perform permission verification
    if check_perms and ALL_PERMISSIONS.isdisjoint(user_perms):
        # Using isdisjoint method is more efficient than set intersection
        if user_perms.isdisjoint(check_perms):
            raise CustomException(
                msg="No permission to operate",
                code=status.HTTP_403_FORBIDDEN
            )


def get_user_permissions(user: User):
    """
    Get user permissions
    :param user: user object
    :return: permissions set
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
    Phone number login
    :param request: request object
    :param db: database session
    :param form_data: form data
    :return: response
    """
    user = get_user_by_telephone(db, form_data.username)
    try:
        # Phone number and password login
        if form_data.platform not in ["0", "1"]:
            raise ValueError("Other platforms are not supported yet")
        if form_data.method != '0':
            raise ValueError("Other login methods are not supported yet")
        if not user:
            raise ValueError("User with this phone number does not exist")
        if not User.verify_password(form_data.password, user.password):
            raise ValueError("Incorrect password")
        if form_data.platform == '0' and not user.is_staff:
            raise ValueError("Must be a platform employee to login to admin backend")

    except ValueError as e:
        return ErrorResponse(str(e))

    return await check_normal_user_login(db, user, request)


async def check_normal_user_login(db, user, request):
    """
    Common verification settings
    :param db: database session
    :param request: request object
    :param user: user object
    :return: response
    """
    try:
        if not user:
            raise ValueError("Phone number does not exist")
        elif user.disabled:
            raise ValueError("Phone number has been frozen")
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
    return SuccessResponse(result, "Login successful")


async def update_login_info(db, user, last_ip: str) -> None:
    """
    Update current login information
    :param db: database session
    :param user: user object
    :param last_ip: last login IP
    :return: None
    """
    user.last_ip = last_ip
    user.last_login_at = datetime.now()
    db.flush()


async def reset_user_current_password(db, u, form_data):
    """
    Reset current user password
    :param db: database session
    :param u: user object
    :param form_data: form data
    :return: None
    """
    if form_data.password != form_data.password_two:
        raise CustomException(msg="Passwords do not match", code=400)

    result = helpers.valid_password(form_data.password)
    if isinstance(result, str):
        raise CustomException(result)

    u.password = User.get_password_hash(form_data.password)
    db.flush(u)


def get_user_by_telephone(db: Session, telephone: str) -> Union[User, None]:
    """Get user object by phone number"""
    return db.query(User).filter(User.telephone == telephone).first()
