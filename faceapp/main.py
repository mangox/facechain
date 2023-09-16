#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from faceapp.resources.inpaint import Inpaint, InpaintList
from faceapp.resources.user import UserResource, UserList
from faceapp.resources.modelscope import ModelScope, ModelScopeList
from faceapp.resources.inference import Inference, InferenceList
from faceapp.config import sqliteConfig
from faceapp import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = sqliteConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension
# app.config["JWT_SECRET_KEY"] = "Dese.Decent.Pups.BOOYO0OST"  # Change this!
# jwt = JWTManager(app)
api = Api(app)


# jwt = JWT(app, authenticate, identity)  # Auto Creates /auth endpoint

api.add_resource(UserResource, '/user/<string:token>')
api.add_resource(UserList, '/users')
api.add_resource(ModelScope, '/modelscope/<string:token>', '/modelscope/<string:token>/<string:output_model_name>')
api.add_resource(ModelScopeList, '/modelscopes')
api.add_resource(Inference, '/inference/<string:token>', '/inference/<string:token>/<string:output_model_name>')
api.add_resource(InferenceList, '/inferences')
api.add_resource(Inpaint, '/inpaint/<string:token>', '/inpaint/<string:token>/<string:output_model_name>')
api.add_resource(InpaintList, '/inpaints')

db.init_db(app)

if __name__ == '__main__':

    # TODO: Add swagger integration
    app.run(debug=True)  # important to mention debug=True
