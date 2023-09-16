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

from faceapp.models.modelscope import ModelScopeModel
from faceapp.util.logz import create_logger


class ModelScope(Resource):
    def __init__(self):
        self.logger = create_logger()

    model_args = {
        "status": fields.Int()
    }

    def get(self, token, output_model_name=None):
        self.logger.info(f"{token} find model {output_model_name}")
        data = parser.parse(self.model_args, request)

        status = data.get('status')
        query_criteria = {'token': token}
        if status:
            query_criteria['status'] = status
        if output_model_name:
            query_criteria['output_model_name'] = output_model_name

        results = ModelScopeModel.query.filter_by(**query_criteria).all()

        return [r.json() for r in results]


class ModelScopeList(Resource):
    def __init__(self):
        self.logger = create_logger()

    model_args = {
        'token':             fields.Str(required=True),
        'base_model_name':   fields.Str(required=True),
        'output_model_name': fields.Str(required=True),

        'upload_images':     fields.Str(required=True),

        'ensemble':          fields.Bool(load_default=False),
        'enhance_lora':      fields.Bool(load_default=False),
    }

    def post(self):
        data = parser.parse(self.model_args, request)
        try:
            token = data['token']
            base_model_name = data['base_model_name']
            output_model_name = data['output_model_name']
            ensemble = data.get('ensemble', False)
            enhance_lora = data.get('enhance_lora', False)
            upload_images = data['upload_images']

            model_scope = ModelScopeModel.query.filter_by(token=token,
                                                          output_model_name=output_model_name).one_or_none()
            if model_scope:
                return jsonify(code=1, msg=f"model {output_model_name} already exists.")

            model = ModelScopeModel(token, base_model_name, output_model_name, ensemble, enhance_lora, upload_images)
            model.save_to_db()

            return model.json()
        except Exception as e:
            return jsonify(code=1, msg=str(e))
