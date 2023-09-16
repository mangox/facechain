#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
# **********************************************************************************************************
# This is the confidential unpublished intellectual property of Bybit Corporation,
# and includes without limitation exclusive copyright and trade secret rights of Bybit throughout the world.
# **********************************************************************************************************
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
