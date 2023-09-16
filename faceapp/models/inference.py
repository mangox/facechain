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
output_model_name： 输出模型名称(必须已经存在）
style_index     ：风格索引
cloth_style_index ： LoRA增强
image_paths  : 图片路径
created: 创建时间
updated：最后更新时间
"""


class InferenceModel(db.Model):
    __tablename__ = 'inference'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), db.ForeignKey('users.token'))
    base_model_name = db.Column(db.String(256))
    output_model_name = db.Column(db.String(256))
    style_model_name = db.Column(db.String(256))
    cloth_style = db.Column(db.String(256))
    style_weight = db.Column(db.String(256))
    human_weight = db.Column(db.String(256))
    pose_image = db.Column(db.String(256))
    pose_model_name = db.Column(db.String(256))
    image_count = db.Column(db.Integer)
    image_results = db.Column(db.Text)
    status = db.Column(db.Integer)

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    user = db.relationship('UserModel')

    def __init__(self, token, base_model_name, output_model_name, style_model_name, cloth_style, style_weight, human_weight,
                 pose_image, pose_model_name, image_count, image_results="", status=0):
        self.token = token
        self.base_model_name = base_model_name
        self.output_model_name = output_model_name

        self.style_model_name = style_model_name
        self.cloth_style = cloth_style
        self.style_weight = style_weight
        self.human_weight = human_weight
        self.pose_image = pose_image
        self.pose_model_name = pose_model_name
        self.image_count = image_count
        self.image_results = image_results

        self.status = status
        self.created = datetime.now()
        self.updated = datetime.now()

    def json(self):
        return {'token': self.token, 'base_model_name': self.base_model_name, 'output_model_name': self.output_model_name,
                'style_model_name': self.style_model_name, 'cloth_style': self.cloth_style,
                'pose_image': self.pose_image, 'pose_model_name': self.pose_model_name,
                'image_count': self.image_count, 'status': self.status, 'image_results': self.image_results,
                'created': int(self.created.timestamp()*1e3), 'updated': int(self.updated.timestamp()*1e3)}

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()  # simple TOP 1 select

    def save_to_db(self):  # Upserting data
        self.updated = datetime.now()

        db.session.add(self)
        db.session.commit()  # Balla

