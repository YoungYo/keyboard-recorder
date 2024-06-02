#!/usr/bin/env python
# coding: utf-8

"""
@author: YoungYo
@file: DbManager
@time: 2024/5/22 17:16
@desc: 数据库连接池
"""
import pymysql
from pymysql import cursors
from dbutils.pooled_db import PooledDB
import datetime


class DbManager(object):
    def __init__(self, a_host, a_user, a_port, pwd, a_db):
        conn_kw_args = {'host': a_host,
                        'user': a_user,
                        'port': a_port,
                        'passwd': pwd,
                        'db': a_db,
                        'charset': 'utf8'}
        self._pool = PooledDB(pymysql, mincached=0, maxcached=10, maxshared=10, maxusage=10000, **conn_kw_args)

    def db_execute(self, sql, *params):
        conn = self._pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute("set names utf8mb4;")
            cursor.execute(sql, params)
            conn.commit()
            affected_rows = cursor.rowcount
        except Exception as e:
            print(e)
            return 0
        finally:
            cursor.close()
            conn.close()
        return affected_rows

    def db_execute_many(self, sql, *params):
        conn = self._pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute("set names utf8mb4;")
            cursor.executemany(sql, params)
            conn.commit()
            affected_rows = cursor.rowcount
        except Exception as e:
            print(e)
            return 0
        finally:
            cursor.close()
            conn.close()
        return affected_rows

    def query_one(self, sql, *params):
        conn = self._pool.connection()
        cursor = conn.cursor(cursors.DictCursor)
        cursor.execute("set names utf8mb4;")
        rowcount = cursor.execute(sql, params)
        if rowcount > 0:
            res = cursor.fetchone()
        else:
            res = None
        cursor.close()
        conn.close()
        return res

    def query_all(self, sql, *params):
        conn = self._pool.connection()
        cursor = conn.cursor(cursors.DictCursor)
        cursor.execute("set names utf8mb4;")
        rowcount = cursor.execute(sql) if len(params) == 0 else cursor.execute(sql, params)
        if rowcount > 0:
            res = cursor.fetchall()
        else:
            res = None
        cursor.close()
        conn.close()
        return res

    def query_count(self, sql, *params):
        result = self.query_one(sql, *params)
        return list(result.values())[0]


def time_str():
    return datetime.datetime.now()
