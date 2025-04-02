# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : views.py
# @desc           : 主配置文件
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from api.admin.logics import system
from api.admin.params.system import UserParams, RoleParams
from api.admin.schemas import system_schemas
from core.database import get_db, get_async_db
from core.dependencies import IdList
from core.exception import CustomException
from core.response import SuccessResponse, ErrorResponse
from models.data_dict import DictType
from services import auth, dict as dictService

systemAPI = APIRouter()


###########################################################
#    user manage
###########################################################
@systemAPI.post("/user", summary="创建用户")
def create_user(form_data: system_schemas.UserRequest,
                db: Session = Depends(get_db),
                u=Depends(auth.get_current_user)
                ):
    return SuccessResponse(system.create_user(db, form_data), message="创建用户完成")


@systemAPI.get("/user", summary="用户列表")
def get_user_list(params: UserParams = Depends(),
                  db: Session = Depends(get_db),
                  u=Depends(auth.get_current_permission_user(['system.user.list']))
                  ):
    total, records = system.get_user_list(db, u, params)
    return SuccessResponse({"total": total, "list": records}, "获取用户列表")


@systemAPI.get("/user/menu", response_model=list[system_schemas.RouterOut], summary="用户菜单目录")
def get_user_menu_tree(db: Session = Depends(get_db),
                       u=Depends(auth.get_current_user)
                       ):
    return SuccessResponse(system.get_user_menu_tree(db, u), "获取用户菜单")


@systemAPI.get("/user/perms", summary="获取用户权限")
def get_user_permissions(u=Depends(auth.get_current_user)):
    return SuccessResponse(list(auth.get_user_permissions(u)), "获取用户权限")


@systemAPI.put("/user/{data_id}", summary="更新用户信息")
def put_user(data_id: int,
             form_data: system_schemas.UserRequest,
             db: Session = Depends(get_db),
             u=Depends(auth.get_current_user)
             ):
    return SuccessResponse(system.put_user(db, u, data_id, form_data), "编辑用户完成")


###########################################################
#    role manage
###########################################################

@systemAPI.get("/role", summary="获取角色列表")
def get_role_list(params: RoleParams = Depends(),
                  db: Session = Depends(get_db),
                  u=Depends(auth.get_current_user)
                  ):
    total, records = system.get_role_list(db, u, params)
    return SuccessResponse({"total": total, "list": records}, "获取角色列表")


@systemAPI.post("/role", summary="创建角色信息")
def create_role(
        form_data: system_schemas.RoleRequest,
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)):
    return SuccessResponse(system.create_role(db, u, form_data), message="创建角色完成")


@systemAPI.delete("/role/{data_id}", summary="删除角色")
def delete_role(
        data_id: int = Path(default=..., description="角色ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)):
    if 1 == data_id:
        return ErrorResponse("不能删除管理员角色")

    return SuccessResponse(system.delete_role(db, u, data_id), message="删除角色完成")


@systemAPI.put("/role/{data_id}", summary="更新角色信息")
def put_role(
        form_data: system_schemas.RoleRequest,
        data_id: int = Path(default=..., description="角色ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    if 1 == data_id:
        return ErrorResponse(message="不能修改管理员角色")

    return SuccessResponse(system.put_role(db, u, data_id, form_data), '更新角色完成')


###########################################################
#    menu manage
###########################################################
@systemAPI.get("/menu", summary="获取菜单列表")
def get_menu_list(
        mode: int = Query(default=1, description="菜单模式 1、菜单列表使用 2、添加角色使用"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(system.get_menu_list(db, u, mode), '获取菜单列表完成')


@systemAPI.post("/menu", summary="创建菜单信息")
def create_menu(
        form_data: system_schemas.Menu,
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)):
    return SuccessResponse(system.create_menu(db, u, form_data), "创建菜单完成")


@systemAPI.delete("/menu/{data_id}", summary="删除菜单")
def delete_menu(
        data_id: int = Path(default=..., description="菜单ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)):
    return SuccessResponse(system.delete_menu(db, u, data_id), "删除菜单完成")


@systemAPI.put("/menu/{data_id}", summary="更新菜单信息")
def put_menu(
        form_data: system_schemas.Menu,
        data_id: int = Path(default=..., description="菜单ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(system.put_menu(db, u, data_id, form_data), "编辑菜单完成")


###########################################################
#    department manage
###########################################################
@systemAPI.get("/department", summary="获取部门列表")
async def get_department_lit(
        mode: int = Query(default=1, description="部门 1、列表使用 2、添加/修改部门使用 3、部门权限时使用"),
        db: Session = Depends(get_async_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(await system.get_department_list(db, u, mode))


@systemAPI.post("/department", summary="创建部门信息")
def create_department(form_data: system_schemas.Department,
                      db: Session = Depends(get_db),
                      u=Depends(auth.get_current_user)
                      ):
    return SuccessResponse(system.create_department(db, u, form_data))


@systemAPI.delete("/department", summary="批量删除部门", description="硬删除, 如果存在用户关联则无法删除")
def delete_department(ids: IdList = Depends(),
                      db: Session = Depends(get_db),
                      u=Depends(auth.get_current_user)):
    return SuccessResponse(system.delete_department(db, ids.ids, v_soft=False), "删除成功")


@systemAPI.put("/department/{data_id}", summary="更新部门信息")
def put_department(
        data_id: int,
        data: system_schemas.Department,
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)):
    return SuccessResponse(system.put_department(db, u, data_id, data))


@systemAPI.get("/dict/list", summary="获取数据字典列表")
def get_dict_list(
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(dictService.get_dict_list(db, u), "获取数据字典列表")


@systemAPI.post("/dict/create", summary="创建字典类型")
def create_dict_tpe(
        form_data: system_schemas.DictTypeRequest,
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(dictService.create_dict_type(db, u, form_data), '创建字典类型完成')


@systemAPI.put("/dict/{data_id}", summary="编辑字典类型")
def update_dict_tpe(
        form_data: system_schemas.DictTypeRequest,
        data_id: int = Path(default=..., description="字典"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(dictService.update_dict_type(db, u, data_id, form_data), '编辑字典类型完成')


@systemAPI.get("/dict/detail/{data_id}", summary="获取字典详情列表")
def get_dict_detail_list(
        data_id: int = Path(default=..., description="字典ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    dict_type = db.query(DictType).get(data_id)
    if not dict_type:
        raise CustomException("未获取到字典类型信息")
    return SuccessResponse(dictService.get_dict_details(db, dict_type.tp), "获取数据字典列表")


@systemAPI.post("/dict/detail/{dict_id}", summary="创建字典详情")
def create_dict_detail(
        form_data: system_schemas.DictDetailRequest,
        dict_id: int = Path(default=..., description="字典ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(dictService.create_dict_detail(db, u, dict_id, form_data), '创建字典详情')


@systemAPI.put("/dict/detail/{detail_id}", summary="编辑字典详情")
def update_dict_detail(
        form_data: system_schemas.DictDetailRequest,
        detail_id: int = Path(default=..., description="详情ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(dictService.update_dict_detail(db, u, detail_id, form_data), '编辑字典详情完成')


@systemAPI.delete("/dict/detail/{detail_id}", summary="删除字典详情")
def delete_dict_detail(
        detail_id: int = Path(default=..., description="详情ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_user)
):
    return SuccessResponse(dictService.delete_dict_detail(db, u, detail_id), '已完成字典详情的删除操作')
