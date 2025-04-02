# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/16
# @File           : initialize.py
# @desc           : 数据初始化
from sqlalchemy import text

from api.admin.logics import system
from api.admin.schemas import system_schemas
from core import database

db = database.session_local()


def migrate():
    print("create system menus")
    create_system_menus()
    print("create system departments")
    create_system_department()
    print("create system roles")
    create_super_role()
    print("create super user")
    create_super_admin()

def create_system_department():
    department = {"name": "Headquarters", "dept_key":"head", "disabled": False, "order": 0, "desc": "Headquarters department"}
    form_data = system_schemas.Department(**department)
    system.create_department(db, None, form_data)
    
def create_super_role():
    role = {"role_key": "admin", "name": "super admin", "disabled": False, "order": 0,"is_admin":1, "desc": "super admin role","menu_ids":[1,2,3,4], "dept_ids":[1]}
    form_data = system_schemas.RoleRequest(**role)
    system.create_role(db, None, form_data)


def create_super_admin():
    user = {"telephone": '13800000000', 'name': 'super admin', 'nickname': "super admin", 'is_staff': True,'role_ids': [1], 'dept_ids': [1]}
    form_data = system_schemas.UserRequest(**user)
    system.create_user(db, form_data)


def create_system_menus():
    # 系统管理
    system_menu = {
        "title": "system manage",
        "name": "System",
        "icon": "ant-design:setting-outlined",
        "path": "/system",
        "component": "BasicLayout",
        "redirect": "/system/menu",
        "menu_type": 0,
        "order": 100,
        "parent_id": None
    }
    system_form = system_schemas.Menu(**system_menu)
    system.create_menu(db, None, system_form)

    # 菜单管理
    menu_menu = {
        "title": "menu manage",
        "name": "SystemMenu",
        "icon": "ant-design:menu-outlined",
        "path": "/system/menu",
        "component": "views/system/menu/index",
        "menu_type": 1,
        "order": 1,
        "parent_id": 1
    }
    menu_form = system_schemas.Menu(**menu_menu)
    system.create_menu(db, None, menu_form)

    # 角色管理
    role_menu = {
        "title": "role manage",
        "name": "SystemRole",
        "icon": "ant-design:user-outlined",
        "path": "/system/role",
        "component": "views/system/role/index",
        "menu_type": 1,
        "order": 2,
        "parent_id": 1
    }
    role_form = system_schemas.Menu(**role_menu)
    system.create_menu(db, None, role_form)

    # 用户管理
    user_menu = {
        "title": "user manage",
        "name": "SystemUser",
        "icon": "ant-design:team-outlined",
        "path": "/system/user",
        "component": "views/system/user/index",
        "menu_type": 1,
        "order": 3,
        "parent_id": 1
    }
    user_form = system_schemas.Menu(**user_menu)
    system.create_menu(db, None, user_form)
