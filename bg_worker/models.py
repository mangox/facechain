#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
# **********************************************************************************************************
# This is the confidential unpublished intellectual property of Bybit Corporation,
# and includes without limitation exclusive copyright and trade secret rights of Bybit throughout the world.
# **********************************************************************************************************

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Text
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from bg_worker.db import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    token = Column(String(256), unique=True)
    score = Column(Integer, default=0)

    def __init__(self, token, score=0):
        self.token = token
        self.score = score

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


class ModelScopeModel(BaseModel):
    __tablename__ = 'model_tasks'

    id = Column(Integer, primary_key=True)
    token = Column(String(256), ForeignKey('users.token'))
    base_model_name = Column(String(256))
    output_model_name = Column(String(256))
    ensemble = Column(Boolean)
    enhance_lora = Column(Boolean)
    upload_images = Column(Text)
    status = Column(Integer)
    created = Column(DateTime)
    updated = Column(DateTime)

    user = relationship('UserModel')

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
        return {'token':             self.token, 'base_model_name': self.base_model_name,
                'output_model_name': self.output_model_name,
                'ensemble':          self.ensemble, 'enhance_lora': self.enhance_lora,
                'upload_images':     self.upload_images,
                'status':            self.status, 'created': int(self.created.timestamp() * 1e3),
                'updated':           int(self.updated.timestamp() * 1e3)}

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()  # simple TOP 1 select


class InpaintModel(BaseModel):
    __tablename__ = 'inpaint'

    id = Column(Integer, primary_key=True)
    token = Column(String(256), ForeignKey('users.token'))
    base_model_name = Column(String(256))
    output_model_name = Column(String(256))

    gallery_template = Column(String(256))
    initial_weight = Column(String(256))
    secondary_weight = Column(String(256))
    fusion_ratio = Column(String(256))
    face_count = Column(Integer)
    fusion_before = Column(String(256))
    fusion_after = Column(String(256))

    image_results = Column(Text)
    status = Column(Integer)

    created = Column(DateTime)
    updated = Column(DateTime)

    user = relationship('UserModel')

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
        return {'token':             self.token, 'base_model_name': self.base_model_name,
                'output_model_name': self.output_model_name,
                'gallery_template':  self.gallery_template, 'initial_weight': self.initial_weight,
                'secondary_weight':  self.secondary_weight, 'fusion_ratio': self.fusion_ratio,
                'face_count':        self.face_count, 'fusion_before': self.fusion_before,
                'fusion_after':      self.fusion_after,
                'status':            self.status, 'image_results': self.image_results,
                'created':           int(self.created.timestamp() * 1e3),
                'updated':           int(self.updated.timestamp() * 1e3)}

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()  # simple TOP 1 select


class InferenceModel(BaseModel):
    __tablename__ = 'inference'

    id = Column(Integer, primary_key=True)
    token = Column(String(256), ForeignKey('users.token'))
    base_model_name = Column(String(256))
    output_model_name = Column(String(256))
    style_model_name = Column(String(256))
    cloth_style = Column(String(256))
    style_weight = Column(String(256))
    human_weight = Column(String(256))
    pose_image = Column(String(256))
    pose_model_name = Column(String(256))
    image_count = Column(Integer)
    image_results = Column(Text)
    status = Column(Integer)

    created = Column(DateTime)
    updated = Column(DateTime)

    user = relationship('UserModel')

    def __init__(self, token, base_model_name, output_model_name, style_model_name, cloth_style, style_weight,
                 human_weight,
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
        return {'token':             self.token, 'base_model_name': self.base_model_name,
                'output_model_name': self.output_model_name,
                'style_model_name':  self.style_model_name, 'cloth_style': self.cloth_style,
                'pose_image':        self.pose_image, 'pose_model_name': self.pose_model_name,
                'image_count':       self.image_count, 'status': self.status, 'image_results': self.image_results,
                'created':           int(self.created.timestamp() * 1e3),
                'updated':           int(self.updated.timestamp() * 1e3)}

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()  # simple TOP 1 select
