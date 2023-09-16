#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports
secret = "xufeiyang_abcd"

mssql = {'host': 'dbhost',
         'user': 'dbuser',
         'passwd': 'dbPwd',
         'db': 'db'}

postgresql = {'host': '0.0.0.0',
         'user': 'postgres',
         'passwd': 'magical_password',
         'db': 'db'}


sqliteConfig = 'sqlite:///database.db'

mssqlConfig = "mssql+pyodbc://{}:{}@{}:1433/{}?driver=SQL+Server+Native+Client+10.0".format(mssql['user'], mssql['passwd'], mssql['host'], mssql['db'])
postgresqlConfig = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])

