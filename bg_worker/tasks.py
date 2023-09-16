#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
# **********************************************************************************************************
# This is the confidential unpublished intellectual property of Bybit Corporation,
# and includes without limitation exclusive copyright and trade secret rights of Bybit throughout the world.
# **********************************************************************************************************
import time
from typing import Union

from bg_worker.logz import create_logger
from bg_worker.models import InferenceModel, InpaintModel, ModelScopeModel
from bg_worker.train_lora import Trainer

logger = create_logger()


def execute_task(model: Union[ModelScopeModel, InferenceModel, InpaintModel]):
    start = time.time()
    if isinstance(model, ModelScopeModel):
        logger.info(f"start to run model scope: {model.json()}")
        run_model_scope(model)
    elif isinstance(model, InferenceModel):
        logger.info(f"start to run inference: {model.json()}")
        run_inference(model)
    elif isinstance(model, InpaintModel):
        logger.info(f"start to run inpaint: {model.json()}")
        run_inpaint(model)
    else:
        logger.error(f"Unknown model: {model.json()}")

    logger.info(f"end, elapsed time: {time.time() - start}")
    return True


def run_model_scope(model: ModelScopeModel):
    # 模型训练
    ret, msg = Trainer.run(model)
    if ret:
        logger.info(msg)
    else:
        logger.error(msg)

    return ret


def run_inference(model: InferenceModel):
    # 无限风格形象写真
    pass


def run_inpaint(model: InpaintModel):
    # 固定模板形象写真
    pass
