#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
# **********************************************************************************************************
# This is the confidential unpublished intellectual property of Bybit Corporation,
# and includes without limitation exclusive copyright and trade secret rights of Bybit throughout the world.
# **********************************************************************************************************

from flask import jsonify, request
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import parser

from faceapp.models.user import UserModel
from faceapp.util.logz import create_logger


class UserResource(Resource):
    def __init__(self):
        self.logger = create_logger()

    def get(self, token):
        user_model = UserModel.query.filter_by(token=token).one_or_none()
        if not user_model:
            return jsonify(code=1, msg="user not found")

        return jsonify(token=token, score=user_model.score)


class UserList(Resource):
    def __init__(self):
        self.logger = create_logger()

    user_args = {
        'token': fields.Str(required=True),
        'score': fields.Int(required=True)
    }

    def post(self):
        data = parser.parse(self.user_args, request)
        token = data['token']
        score = data['score']

        user_model = UserModel.query.filter_by(token=token).one_or_none()
        if not user_model:
            user_model = UserModel(token, score=score)
        else:
            user_model.score += score

        try:
            user_model.save_to_db()
        except:
            return {"code": 1001, "message": "An error occurred inserting the item."}

        return jsonify(token=token, score=user_model.score)
