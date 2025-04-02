# -*- coding: UTF-8 -*-
# @Project ：Apartment-partner-server 
# @version : 1.0
# @File    ：dict.py
# @Author  ：ben
# @Date    ：2025/3/6 上午10:19 
# @desc    : 数据字典
from core.exception import CustomException
from models.data_dict import DictType, DictDetails
from utils import helpers


def get_dict_list(db, u):
    """
    获取字典列表
    :param db:
    :param u:
    :return:
    """
    dict_tp_list = db.query(DictType).all()
    result = []
    for dict_tp in dict_tp_list:
        tmp = {
            "id": dict_tp.id,
            "name": dict_tp.name,
            "tp": dict_tp.tp,
            "disabled": dict_tp.disabled,
            "remark": dict_tp.remark if dict_tp.remark else "",
            "created_at": helpers.date2str(dict_tp.created_at),
            "details": [{"id": dt.id, "value": dt.value, "label": dt.label} for dt in dict_tp.details],
        }
        result.append(tmp)
    return result


def get_dict_details(db, tp):
    dict_tp = db.query(DictType).filter(DictType.tp == tp).first()
    result = []
    for item in dict_tp.details:
        result.append({"id": item.id,
                       "value": item.value,
                       "label": item.label,
                       "is_default": item.is_default,
                       "disabled": item.disabled,
                       "order": item.order,
                       "created_at": helpers.date2str(item.created_at),
                       })

    return sorted(result, key=lambda dt: dt['order'])


def create_dict_type(db, u, form_data):
    cnt = db.query(DictType).where(DictType.tp == form_data.tp).count()
    if cnt:
        raise CustomException("已存在该标识不能创建")
    dt = DictType(**form_data.model_dump())
    db.add(dt)
    db.commit()


def get_dict_single_default(db, tp, label):
    """
    获取字典某个详情
    """
    dict_tp = db.query(DictType).filter(DictType.tp == tp).first()
    if not dict_tp:
        return None
    detail = db.query(DictDetails).filter(
        DictDetails.dict_type_id == dict_tp.id,
        DictDetails.label == label).first()
    return detail.value if detail else None


def update_dict_type(db, u, data_id, form_data):
    dt = db.query(DictType).get(data_id)
    if not dt:
        raise CustomException("不存在该字典类型")
    dt.tp = form_data.tp
    dt.disabled = form_data.disabled
    dt.remark = form_data.remark
    dt.name = form_data.name
    db.commit()


def create_dict_detail(db, u, data_id, form_data):
    dict_type = db.query(DictType).get(data_id)
    if not dict_type:
        raise CustomException("未获取到字典类型")
    data = form_data.model_dump()
    data['dict_type_id'] = data_id
    dt = DictDetails(**data)
    db.add(dt)
    db.commit()


def update_dict_detail(db, u, data_id, form_data):
    de = db.query(DictDetails).get(data_id)
    if not de:
        raise CustomException("字典详情不存在")
    de.value = form_data.value
    de.disabled = form_data.disabled
    de.label = form_data.label
    de.is_default = form_data.is_default
    de.order = form_data.order
    db.commit()


def delete_dict_detail(db, u, detail_id):
    """
    删除字典详情
    """
    de = db.query(DictDetails).get(detail_id)
    if not de:
        raise CustomException("字典详情不存在")
    db.delete(de)
    db.commit()
