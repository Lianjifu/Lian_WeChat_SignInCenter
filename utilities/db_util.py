#!/usr/bin/python
# encoding=utf-8
# Python 和 MySQL 交互
import MySQLdb
# 切换数据库环境变量
from config import *


class db_util(object):
    def __init__(self, db_host=db_host, db_usr=db_usr, db_pw=db_pw, db_charset=db_charset, db_port=db_port,
                 pps_db=pps_db, db_curclass=None):
        conn = None
        cur = None
        try:
            conn = MySQLdb.connect(db_host, db_usr, db_pw, charset=db_charset, port=db_port)
            conn.select_db(pps_db)
            if db_curclass:
                cur = conn.cursor()
            else:
                cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        except Exception, e:
            conn = None
            cur = None

        self.conn = conn
        self.cur = cur

    def selectSQL(self, _sql_str=None, _tuple=None, _type=0):
        db_result = ()
        if _sql_str:
            try:
                if _type == 0:
                    if _tuple:
                        self.cur.execute(_sql_str, _tuple)
                        db_result = self.cur.fetchone()
                    else:
                        self.cur.execute(_sql_str)
                        db_result = self.cur.fetchone()
                else:
                    if _tuple:
                        self.cur.execute(_sql_str, _tuple)
                        db_result = self.cur.fetchall()
                    else:
                        self.cur.execute(_sql_str)
                        db_result = self.cur.fetchall()

            except Exception, e:
                db_result = ()
        else:
            pass
        return db_result

    def executeSQL(self, _sql_str=None, _tuple=None):
        db_result = 0
        if _sql_str:
            try:
                if _tuple:
                    db_result = self.cur.execute(_sql_str, _tuple)
                else:
                    db_result = self.cur.execute(_sql_str)
            except Exception, e:
                print "executeSQL error: ", e
                db_result = 0
        else:
            pass
        return db_result

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()


    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
