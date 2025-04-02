# -*- coding: UTF-8 -*-
# @Project ：rent_house 
# @version : 1.0
# @File    ：routers.py
# @Author  ：ben
# @Date    ：2025/4/2 下午1:37 
# @desc    : route urls

from api.admin import *

urlpatterns = [
    # admin system route
    {"ApiRouter": adminSystemAPI, "prefix": "/api/admin/system", "tags": ["admin-permission manage"]},
]