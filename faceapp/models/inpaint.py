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
gallery_template  ：艺术照模板
initial_weight: 初始权重0.45
secondary_weight: 二次权重0.1
fusion_ratio: 融合系数 0.5
face_count: 生成数目 1
fusion_before: 前融合 true/false
fusion_after: 后融合  true/false
status: 状态 0
image_results: 结果
created: 创建时间
updated：最后更新时间
"""


class InpaintModel(db.Model):
    __tablename__ = 'inpaint'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), db.ForeignKey('users.token'))
    base_model_name = db.Column(db.String(256))
    output_model_name = db.Column(db.String(256))

    gallery_template = db.Column(db.String(256))
    initial_weight = db.Column(db.String(256))
    secondary_weight = db.Column(db.String(256))
    fusion_ratio = db.Column(db.String(256))
    face_count = db.Column(db.Integer)
    fusion_before = db.Column(db.String(256))
    fusion_after = db.Column(db.String(256))

    image_results = db.Column(db.Text)
    status = db.Column(db.Integer)

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    user = db.relationship('UserModel')

    def __init__(self, token, base_model_name, output_model_name, gallery_template, initial_weight, secondary_weight,
                 fusion_ratio, face_count, fusion_before, fusion_after, image_results, status=0):
        self.token = token
        self.base_model_name = base_model_name
        self.output_model_name = output_model_name

        self.gallery_template = gallery_template
        self.initial_weight = initial_weight
        self.secondary_weight = secondary_weight
        self.fusion_ratio = fusion_ratio
        self.face_count = face_count
        self.fusion_before = fusion_before
        self.fusion_before = fusion_before
        self.fusion_after = fusion_after
        self.image_results = image_results

        self.status = status
        self.created = datetime.now()
        self.updated = datetime.now()

    def json(self):
        return {'token': self.token, 'base_model_name': self.base_model_name, 'output_model_name': self.output_model_name,
                'gallery_template': self.gallery_template, 'initial_weight': self.initial_weight,
                'secondary_weight': self.secondary_weight, 'fusion_ratio': self.fusion_ratio,
                'face_count': self.face_count, 'fusion_before': self.fusion_before, 'fusion_after': self.fusion_after,
                'status': self.status, 'image_results': self.image_results,
                'created': int(self.created.timestamp()*1e3), 'updated': int(self.updated.timestamp()*1e3)}

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()  # simple TOP 1 select

    def save_to_db(self):  # Upserting data
        self.updated = datetime.now()

        db.session.add(self)
        db.session.commit()  # Balla

