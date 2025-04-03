# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/12
# @File           : views.py
# @desc           : Main configuration file
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
@systemAPI.post("/user", summary="Create user")
def create_user(form_data: system_schemas.UserRequest,
                db: Session = Depends(get_db),
                u=Depends(auth.get_current_permission_user(['system.user.create']))
                ):
    return SuccessResponse(system.create_user(db, form_data), message="User created successfully")


@systemAPI.get("/user", summary="User list")
def get_user_list(params: UserParams = Depends(),
                  db: Session = Depends(get_db),
                  u=Depends(auth.get_current_permission_user(['system.user.index']))
                  ):
    total, records = system.get_user_list(db, u, params)
    return SuccessResponse({"total": total, "list": records}, "User list retrieved")


@systemAPI.get("/user/menu", response_model=list[system_schemas.RouterOut], summary="User menu")
def get_user_menu_tree(db: Session = Depends(get_db),
                       u=Depends(auth.get_current_user)
                       ):
    return SuccessResponse(system.get_user_menu_tree(db, u), "User menu retrieved")


@systemAPI.get("/user/perms", summary="Get user permissions")
def get_user_permissions(u=Depends(auth.get_current_user)):
    return SuccessResponse(list(auth.get_user_permissions(u)), "User permissions retrieved")


@systemAPI.put("/user/{data_id}", summary="Update user information")
def put_user(data_id: int,
             form_data: system_schemas.UserRequest,
             db: Session = Depends(get_db),
             u=Depends(auth.get_current_permission_user(['system.user.edit']))
             ):
    return SuccessResponse(system.put_user(db, u, data_id, form_data), "User updated successfully")


###########################################################
#    role manage
###########################################################

@systemAPI.get("/role", summary="Get role list")
def get_role_list(params: RoleParams = Depends(),
                  db: Session = Depends(get_db),
                  u=Depends(auth.get_current_permission_user(['system.role.list']))
                  ):
    total, records = system.get_role_list(db, u, params)
    return SuccessResponse({"total": total, "list": records}, "Role list retrieved")


@systemAPI.post("/role", summary="Create role")
def create_role(
        form_data: system_schemas.RoleRequest,
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.role.create']))):
    return SuccessResponse(system.create_role(db, u, form_data), message="Role created successfully")


@systemAPI.delete("/role/{data_id}", summary="Delete role")
def delete_role(
        data_id: int = Path(default=..., description="Role ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.role.delete']))):
    if 1 == data_id:
        return ErrorResponse("Cannot delete admin role")

    return SuccessResponse(system.delete_role(db, u, data_id), message="Role deleted successfully")


@systemAPI.put("/role/{data_id}", summary="Update role information")
def put_role(
        form_data: system_schemas.RoleRequest,
        data_id: int = Path(default=..., description="Role ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.role.put']))
):
    if 1 == data_id:
        return ErrorResponse(message="Cannot modify admin role")

    return SuccessResponse(system.put_role(db, u, data_id, form_data), 'Role updated successfully')


###########################################################
#    menu manage
###########################################################
@systemAPI.get("/menu", summary="Get menu list")
def get_menu_list(
        mode: int = Query(default=1, description="Menu mode 1: for menu list, 2: for adding roles"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.menu.index']))
):
    return SuccessResponse(system.get_menu_list(db, u, mode), 'Menu list retrieved')


@systemAPI.post("/menu", summary="Create menu")
def create_menu(
        form_data: system_schemas.Menu,
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.user.create']))):
    return SuccessResponse(system.create_menu(db, u, form_data), "Menu created successfully")


@systemAPI.delete("/menu/{data_id}", summary="Delete menu")
def delete_menu(
        data_id: int = Path(default=..., description="Menu ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.menu.delete']))):
    return SuccessResponse(system.delete_menu(db, u, data_id), "Menu deleted successfully")


@systemAPI.put("/menu/{data_id}", summary="Update menu information")
def put_menu(
        form_data: system_schemas.Menu,
        data_id: int = Path(default=..., description="Menu ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.menu.put']))
):
    return SuccessResponse(system.put_menu(db, u, data_id, form_data), "Menu updated successfully")


###########################################################
#    department manage
###########################################################
@systemAPI.get("/department", summary="Get department list")
async def get_department_lit(
        mode: int = Query(default=1, description="Department mode 1: for list, 2: for add/edit, 3: for department permissions"),
        db: Session = Depends(get_async_db),
        u=Depends(auth.get_current_permission_user(['system.department.index'])),
):
    return SuccessResponse(await system.get_department_list(db, u, mode))


@systemAPI.post("/department", summary="Create department")
def create_department(form_data: system_schemas.Department,
                      db: Session = Depends(get_db),
                      u=Depends(auth.get_current_permission_user(['system.department.create']))
                      ):
    return SuccessResponse(system.create_department(db, u, form_data))


@systemAPI.delete("/department", summary="Batch delete department", description="Hard delete, cannot delete if users are associated")
def delete_department(ids: IdList = Depends(),
                      db: Session = Depends(get_db),
                      u=Depends(auth.get_current_permission_user(['system.department.delete']))):
    return SuccessResponse(system.delete_department(db, ids.ids, v_soft=False), "Deleted successfully")


@systemAPI.put("/department/{data_id}", summary="Update department information")
def put_department(
        data_id: int,
        data: system_schemas.Department,
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.department.put']))):
    return SuccessResponse(system.put_department(db, u, data_id, data))


###########################################################
#    dict manage
###########################################################

@systemAPI.get("/dict/list", summary="Get dictionary list")
def get_dict_list(
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.dict.index']))
):
    return SuccessResponse(dictService.get_dict_list(db, u), "Dictionary list retrieved")


@systemAPI.post("/dict/create", summary="Create dictionary type")
def create_dict_tpe(
        form_data: system_schemas.DictTypeRequest,
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.dict.create']))
):
    return SuccessResponse(dictService.create_dict_type(db, u, form_data), 'Dictionary type created successfully')


@systemAPI.put("/dict/{data_id}", summary="Update dictionary type")
def put_dict(
        form_data: system_schemas.DictTypeRequest,
        data_id: int = Path(default=..., description="Dictionary"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.dict.put']))
):
    return SuccessResponse(dictService.update_dict_type(db, u, data_id, form_data), 'Dictionary type updated successfully')


@systemAPI.get("/dict/detail/{data_id}", summary="Get dictionary detail list")
def get_dict_detail_list(
        data_id: int = Path(default=..., description="Dictionary ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.dict_detail.index']))
):
    dict_type = db.query(DictType).get(data_id)
    if not dict_type:
        raise CustomException("Dictionary type not found")
    return SuccessResponse(dictService.get_dict_details(db, dict_type.tp), "Dictionary detail list retrieved")


@systemAPI.post("/dict/detail/{dict_id}", summary="Create dictionary detail")
def create_dict_detail(
        form_data: system_schemas.DictDetailRequest,
        dict_id: int = Path(default=..., description="Dictionary ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.dict_detail.create']))
):
    return SuccessResponse(dictService.create_dict_detail(db, u, dict_id, form_data), 'Dictionary detail created successfully')


@systemAPI.put("/dict/detail/{detail_id}", summary="Update dictionary detail")
def update_dict_detail(
        form_data: system_schemas.DictDetailRequest,
        detail_id: int = Path(default=..., description="Detail ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.dict_detail.put']))
):
    return SuccessResponse(dictService.update_dict_detail(db, u, detail_id, form_data), 'Dictionary detail updated successfully')


@systemAPI.delete("/dict/detail/{detail_id}", summary="Delete dictionary detail")
def delete_dict_detail(
        detail_id: int = Path(default=..., description="Detail ID"),
        db: Session = Depends(get_db),
        u=Depends(auth.get_current_permission_user(['system.dict_detail.delete']))
):
    return SuccessResponse(dictService.delete_dict_detail(db, u, detail_id), 'Dictionary detail deleted successfully')
