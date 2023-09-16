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

from faceapp.models.inpaint import InpaintModel
from faceapp.util.logz import create_logger


class Inpaint(Resource):
    def __init__(self):
        self.logger = create_logger()

    inpaint_args = {
        "status": fields.Int()
    }

    def get(self, token, output_model_name=None):
        self.logger.info(f"{token} find model {output_model_name}")
        data = parser.parse(self.inpaint_args, request)

        status = data.get('status')
        query_criteria = {'token': token}
        if status:
            query_criteria['status'] = status
        if output_model_name:
            query_criteria['output_model_name'] = output_model_name

        results = InpaintModel.query.filter_by(**query_criteria).all()

        return [r.json() for r in results]


class InpaintList(Resource):
    def __init__(self):
        self.logger = create_logger()

    inpaint_args = {
        'token': fields.Str(required=True),
        'base_model_name': fields.Str(required=True),
        'output_model_name': fields.Str(required=True),
        'gallery_template': fields.Str(required=True),
        'initial_weight': fields.Str(load_default="0.45"),
        'secondary_weight': fields.Str(load_default="0.1"),
        'fusion_ratio': fields.Str(load_default="0.5"),
        'face_count': fields.Int(load_default=1),
        'fusion_before': fields.Bool(load_default=True),
        'fusion_after': fields.Bool(load_default=True)
    }

    def post(self):
        data = parser.parse(self.inpaint_args, request)
        try:
            token = data['token']
            base_model_name = data['base_model_name']
            output_model_name = data['output_model_name']

            gallery_template = data['gallery_template']
            initial_weight = data['initial_weight']
            secondary_weight = data['secondary_weight']
            fusion_ratio = data['fusion_ratio']
            fusion_before = data['fusion_before']
            fusion_after = data['fusion_after']
            face_count = data.get('face_count', 1)

            # todo 幂等
            model_scope = InpaintModel.query.filter_by(token=token, output_model_name=output_model_name).one_or_none()
            if model_scope:
                return jsonify(code=1, msg=f"model {output_model_name} already exists.")

            model = InpaintModel(token, base_model_name, output_model_name,
                                 gallery_template, initial_weight, secondary_weight, fusion_ratio, face_count,
                                 fusion_before, fusion_after, "")
            model.save_to_db()

            return model.json()
        except Exception as e:
            return jsonify(code=1, msg=str(e))
