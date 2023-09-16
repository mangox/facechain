#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
# **********************************************************************************************************
# This is the confidential unpublished intellectual property of Bybit Corporation,
# and includes without limitation exclusive copyright and trade secret rights of Bybit throughout the world.
# **********************************************************************************************************
from datetime import datetime

from faceapp.db import db

"""
token : 对应账号
base_model_name(model_id)：基模型id
output_model_name： 输出模型名称
ensemble     ：人物LoRA融合
enhance_lora ： LoRA增强
image_paths  : 图片路径
created: 创建时间
updated：最后更新时间
"""


class ModelScopeModel(db.Model):
    __tablename__ = 'model_tasks'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), db.ForeignKey('users.token'))
    base_model_name = db.Column(db.String(256))
    output_model_name = db.Column(db.String(256))
    ensemble = db.Column(db.Boolean)
    enhance_lora = db.Column(db.Boolean)
    upload_images = db.Column(db.Text)
    status = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    user = db.relationship('UserModel')

    def __init__(self, token, base_model_name, output_model_name, ensemble, enhance_lora, upload_images, status=0):
        self.token = token
        self.base_model_name = base_model_name
        self.output_model_name = output_model_name
        self.enhance_lora = enhance_lora
        self.ensemble = ensemble
        self.upload_images = upload_images
        self.status = status
        self.created = datetime.now()
        self.updated = datetime.now()

    def json(self):
        return {'token': self.token, 'base_model_name': self.base_model_name, 'output_model_name': self.output_model_name,
                'ensemble': self.ensemble, 'enhance_lora': self.enhance_lora, 'upload_images': self.upload_images,
                'status': self.status, 'created': int(self.created.timestamp()*1e3), 'updated': int(self.updated.timestamp()*1e3)}

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()  # simple TOP 1 select

    def save_to_db(self):  # Upserting data
        self.updated = datetime.now()

        db.session.add(self)
        db.session.commit()  # Balla

