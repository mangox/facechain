#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from faceapp.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True)
    score = db.Column(db.Integer, default=0)

    def __init__(self, token, score=0):
        self.token = token
        self.score = score

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter_by(token=token).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

