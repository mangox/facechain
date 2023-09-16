#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
# **********************************************************************************************************
# This is the confidential unpublished intellectual property of Bybit Corporation,
# and includes without limitation exclusive copyright and trade secret rights of Bybit throughout the world.
# **********************************************************************************************************
import sys
import time
from typing import List, Union

from bg_worker.db import DBSession
from bg_worker.models import ModelScopeModel, UserModel, InferenceModel, InpaintModel
from bg_worker.logz import create_logger
from bg_worker.tasks import execute_task

logger = create_logger()


def fetch_model_scope_tasks(session: DBSession) -> List[ModelScopeModel]:
    model_scopes = session.query(ModelScopeModel).filter(ModelScopeModel.status == 0).order_by(ModelScopeModel.id)
    return model_scopes


def fetch_inference_tasks(session: DBSession) -> List[InferenceModel]:
    inferences = session.query(InferenceModel).filter(InferenceModel.status == 0).order_by(InferenceModel.id)
    return inferences


def fetch_inpaint_tasks(session: DBSession) -> List[InpaintModel]:
    inpaints = session.query(InpaintModel).filter(InpaintModel.status == 0).order_by(InpaintModel.id)
    return inpaints


def get_user(session, token) -> UserModel:
    user = session.query(UserModel).filter(UserModel.token == token).one_or_none()
    if user is None:
        logger.error(f"user {token} not exist")

    return user


def check_user(user: UserModel):
    if user is None:
        # 未知用户，任务失败
        return False, 2

    if user.score - 1 < 0:
        # 用户积分不足
        return False, 3

    return True, 0


def user_score_decrease(session, user: UserModel):
    user.score -= 1
    session.commit()


def main():
    tasks = []
    with DBSession() as session:
        tasks.extend(fetch_model_scope_tasks(session))
        tasks.extend(fetch_inference_tasks(session))
        tasks.extend(fetch_inpaint_tasks(session))

        tasks.sort(key=lambda m: m.created)

        while tasks:
            model = tasks.pop(0)

            user = get_user(session, model.token)
            ret, status = check_user(user)
            if not ret:
                model.status = status
                session.commit()
                continue

            ret = execute_task(model)

            if ret:
                user.score -= 1
                logger.info(f"User {user.token}, score(-1): {user.score}, task: {model.__tablename__}:{model.id}")

            session.commit()

    return 0


if __name__ == '__main__':
    sys.exit(main())
