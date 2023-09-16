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

from faceapp.models.inference import InferenceModel
from faceapp.util.logz import create_logger


class Inference(Resource):
    def __init__(self):
        self.logger = create_logger()

    inference_args = {
        # "access_token": fields.Str(required=True),
        # "timestamp": fields.Int(required=True),
        "status": fields.Int()
    }

    def get(self, token, output_model_name=None):
        self.logger.info(f"{token} find model {output_model_name}")
        data = parser.parse(self.inference_args, request)

        status = data.get('status')
        query_criteria = {'token': token}
        if status:
            query_criteria['status'] = status
        if output_model_name:
            query_criteria['output_model_name'] = output_model_name

        results = InferenceModel.query.filter_by(**query_criteria).all()

        return [r.json() for r in results]


class InferenceList(Resource):
    def __init__(self):
        self.logger = create_logger()

    inference_args = {
        'token':             fields.Str(required=True),
        'base_model_name':   fields.Str(required=True),
        'output_model_name': fields.Str(required=True),

        'style_model_name':  fields.Str(required=True),
        'cloth_style':       fields.Str(load_default=""),
        'style_weight':      fields.Str(load_default="0.25"),
        'human_weight':      fields.Str(load_default="0.95"),
        'pose_image':        fields.Str(required=True),
        'pose_model_name':   fields.Str(load_default="no"),
        'image_count':       fields.Int(load_default=6)
    }

    def post(self):
        data = parser.parse(self.inference_args, request)
        try:
            token = data['token']
            base_model_name = data['base_model_name']
            output_model_name = data['output_model_name']

            style_model_name = data['style_model_name']
            cloth_style = data['cloth_style']
            style_weight = data['style_weight']
            human_weight = data['human_weight']
            pose_model_name = data['pose_model_name']
            pose_image = data['pose_image']
            image_count = data.get('image_count', 3)

            model_scope = InferenceModel.query.filter_by(token=token, output_model_name=output_model_name).one_or_none()
            if model_scope:
                return jsonify(code=1, msg=f"model {output_model_name} already exists.")

            model = InferenceModel(token, base_model_name, output_model_name, style_model_name, cloth_style,
                                   style_weight, human_weight, pose_image, pose_model_name, image_count, "")
            model.save_to_db()

            return model.json()
        except Exception as e:
            return jsonify(code=1, msg=str(e))
