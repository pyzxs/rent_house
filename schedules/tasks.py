# -*- coding: utf-8 -*-
# @Project        : Apartment-partner-server
# @version        : 1.0
# @Create Time    : 2025/2/15
# @File           : tasks.py
# @desc           : consumers

from sqlalchemy.orm import scoped_session

from core import database
from schedules import app

session_local = scoped_session(database.session_local)


@app.task
def test_task_run():
    """
    :return:
    """
    db = session_local()
    try:
        pass
    except Exception as e:
        db.rollback()
        raise e
    finally:
        session_local.remove()
