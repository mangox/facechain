#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
# **********************************************************************************************************
# This is the confidential unpublished intellectual property of Bybit Corporation,
# and includes without limitation exclusive copyright and trade secret rights of Bybit throughout the world.
# **********************************************************************************************************
import hashlib
from faceapp.config import secret


def check_auth(data: dict):
    access_token, timestamp = data['access_token'], data['timestamp']
    md5 = hashlib.md5()
    md5.update(f"{secret}{timestamp}".encode())
    expected_token = md5.hexdigest()
    return access_token == expected_token
