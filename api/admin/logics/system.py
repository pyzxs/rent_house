# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/14
# @File           : system.py
# @desc           : 系统管理模块
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.admin.schemas import system_schemas
from config import settings
from core.curd import get_filter_where, order_by
from core.exception import CustomException
from models.data_dict import DictType
from models.user import User, Role, Menu
from utils import helpers


def create_user(db, form_data):
    exists = db.query(User).filter_by(telephone=form_data.telephone).count()
    if exists:
        raise CustomException("手机号码已存在")

    if not form_data.password:
        if settings.DEFAULT_PASSWORD == "0":
            form_data.password = form_data.telephone[5:12]
        else:
            form_data.password = settings.DEFAULT_PASSWORD

    form_data.password = User.get_password_hash(form_data.password)
    form_data.avatar = form_data.avatar if form_data.avatar else settings.DEFAULT_AVATAR
    user = User(**form_data.model_dump(exclude={'role_ids'}))
    if form_data.role_ids:
        roles = db.query(Role).filter(Role.id.in_(form_data.role_ids)).all()
        for role in roles:
            user.roles.add(role)
    db.add(user)
    db.commit()


def put_user(db, u, data_id, form_data):
    user = db.query(User).filter_by(id=data_id).first()
    if not user:
        raise CustomException("该用户不存在")

    exists = db.query(User).filter(User.id != data_id, User.telephone == form_data.telephone).count()
    if exists:
        raise CustomException("该手机已被其它用户占用")

    if not form_data.password:
        if settings.DEFAULT_PASSWORD == "0":
            form_data.password = form_data.telephone[5:12]
        else:
            form_data.password = settings.DEFAULT_PASSWORD

    form_data.password = User.get_password_hash(form_data.password)
    form_data.avatar = form_data.avatar if form_data.avatar else settings.DEFAULT_AVATAR
    data = form_data.model_dump(exclude={'role_ids'})

    for key, value in data.items():
        if key in User.get_column_attrs():
            setattr(user, key, value)  # 使用setattr动态设置属性

    if form_data.role_ids:
        roles = db.query(Role).filter(Role.id.in_(form_data.role_ids)).all()
        user.roles.clear()
        for role in roles:
            user.roles.add(role)
    db.commit()


def get_user_list(db, u, params):
    query = db.query(User)
    conditions = get_filter_where(User, **params.to_where())
    if conditions:
        query = query.filter(*conditions)

    query = order_by(query, User, params.dict())
    total = query.count()
    query = query.options(joinedload(User.roles))
    records = query.offset(params.offset).limit(params.limit).all()
    result = []
    for item in records:
        r = system_schemas.UserResponse.model_validate(item).model_dump()
        r['created_at'] = helpers.date2str(item.created_at)
        r['roles'] = [{"id": role.id, "name": role.name, "key": role.role_key} for role in item.roles]
        result.append(r)

    return total, result


def get_role_list(db, u, params):
    query = db.query(Role)
    conditions = get_filter_where(Role, **params.to_where())
    if conditions:
        query = query.filter(*conditions)

    query = order_by(query, Role, params.dict())
    total = query.count()
    records = query.offset(params.offset).limit(params.limit).all()
    result = []
    for item in records:
        tmp = {"id": item.id, "role_key": item.role_key, "name": item.name, "disabled": item.disabled,
               "order": item.order, "desc": item.desc,
               "is_admin": item.is_admin, 'created_at': helpers.date2str(item.created_at),
               "menu_ids": [menu.id for menu in item.menus if menu.parent_id is not None],
               'updated_at': helpers.date2str(item.updated_at)}
        result.append(tmp)

    return total, result


def create_role(db, u, form_data):
    exists = db.query(Role).filter_by(role_key=form_data.role_key).count()
    if exists:
        raise CustomException(f"已存在角色{form_data.role_key}")

    role = Role(**form_data.model_dump(exclude={'menu_ids'}))
    if form_data.menu_ids:
        role.menus.clear()
        menus = db.query(Menu).filter(Menu.id.in_(form_data.menu_ids)).all()
        for menu in menus:
            role.menus.add(menu)
    db.add(role)
    db.commit()


def put_role(db, u, data_id, form_data):
    role = db.query(Role).filter_by(id=data_id).first()
    if not role:
        raise CustomException("该角色不存在")
    exists = db.query(Role).filter(Role.id != data_id, Role.role_key == form_data.role_key).count()
    if exists:
        raise CustomException(f"已存在角色{form_data.role_key}")

    data = form_data.model_dump(exclude={'menu_ids'})
    for key, value in data.items():
        if key in Role.get_column_attrs():
            setattr(role, key, value)  # 使用setattr动态设置属性

    role.menus.clear()
    if form_data.menu_ids:
        menus = db.query(Menu).filter(Menu.id.in_(form_data.menu_ids)).all()
        for menu in menus:
            role.menus.add(menu)
    db.commit()


def delete_role(db, u, data_id):
    role = db.query(Role).options(joinedload(Role.menus)).get(data_id)
    if role is None:
        raise CustomException("该角色不存在")

    role.menus.clear()
    db.delete(role)
    db.commit()


def get_menu_list(db, u, mode: int):
    """
    1：获取菜单树列表
    2：获取菜单树列表，角色添加菜单权限时使用
    :param db:
    :param mode:
    :return:
    """
    if mode == 3:
        sql = select(Menu).where(Menu.disabled == 0, Menu.deleted_at.is_(None))
    else:
        sql = select(Menu).where(Menu.deleted_at.is_(None))
    queryset = db.scalars(sql)
    datas = list(queryset.all())
    roots = filter(lambda i: not i.parent_id, datas)
    if mode == 1:
        menus = generate_tree_list(datas, roots)
    elif mode == 2:
        menus = generate_tree_options(datas, roots)
    else:
        raise CustomException("获取菜单失败，无可用选项")
    return Menu.menus_order(menus)


def create_menu(db, u, form_data):
    if form_data.parent_id == 0:
        form_data.parent_id = None
    exists = db.query(Menu).filter(Menu.path == form_data.path).count()
    if exists:
        raise CustomException("路由地址不能重复")

    menu = Menu(**form_data.model_dump())
    db.add(menu)
    db.commit()


def delete_menu(db, u, data_id):
    menu = db.query(Menu).get(data_id)
    if not menu:
        raise CustomException("菜单不存在")
    exists = db.query(Menu).filter(Menu.parent_id == menu.id).count()
    if exists:
        raise CustomException("存在子菜单，不能删除")
    db.delete(menu)
    db.commit()


def put_menu(db, u, data_id, form_data):
    menu = db.query(Menu).filter_by(id=data_id).first()
    if not menu:
        raise CustomException("该菜单不存在")

    exists = db.query(Menu).filter(Menu.path == form_data.path, Menu.id != data_id).count()
    if exists:
        raise CustomException("路由地址不能重复")

    if form_data.parent_id == 0:
        form_data.parent_id = None

    data = form_data.model_dump()
    for key, value in data.items():
        if key in Menu.get_column_attrs():
            setattr(menu, key, value)
    db.commit()


def get_user_menu_tree(db, user: User):
    if any([i.is_admin for i in user.roles]):
        sql = select(Menu).where(Menu.disabled == 0, Menu.menu_type.in_([0, 1]), Menu.deleted_at.is_(None))
        queryset = db.scalars(sql)
        datas = list(queryset.all())
    else:
        options = [joinedload(User.roles).subqueryload(Role.menus)]
        user = db.query(User).options(options).get(user.id)
        datas = set()
        for role in user.roles:
            for menu in role.menus:
                # 非禁用并显示的所有惨淡
                if not menu.disabled:
                    datas.add(menu)
    roots = filter(lambda i: not i.parent_id, datas)
    menus = generate_router_tree(datas, roots)
    return Menu.menus_order(menus, 'index')


def generate_router_tree(menus: list[Menu], nodes: filter):
    """
    生成路由树
    :param menus: 总菜单列表
    :param nodes: 节点菜单列表
    :return:
    """

    data = []
    for root in nodes:
        router = system_schemas.RouterOut.model_validate(root)
        router.name = root.name
        router.index = root.order
        router.meta = system_schemas.Meta(
            title=root.title,
            icon=root.icon,
            hideInMenu=root.hidden,
            affixTab=root.affix,
            order=root.order,
            keepAlive=root.no_cache
        )
        sons = filter(lambda i: i.parent_id == root.id, menus)
        router.children = generate_router_tree(menus, sons)
        data.append(router.model_dump())
    return data


def generate_tree_list(menus: list, nodes: filter) -> list:
    """
    生成菜单树列表
    :param menus: 总菜单列表
    :param nodes: 每层节点菜单列表
    :return:
    """
    data = []
    for root in nodes:
        router = system_schemas.MenuTreeResponse.from_orm(root)
        sons = filter(lambda i: i.parent_id == root.id, menus)
        router.children = generate_tree_list(menus, sons)
        data.append(router.model_dump())
    return data


def generate_tree_options(menus: list, nodes: filter):
    """
    生成菜单树选择项
    :param menus:总菜单列表
    :param nodes:每层节点菜单列表
    :return:
    """
    data = []
    for root in nodes:
        router = {"value": root.id, "label": root.title, "order": root.order}
        sons = filter(lambda i: i.parent_id == root.id, menus)
        router["children"] = generate_tree_options(menus, sons)
        data.append(router)
    return data
