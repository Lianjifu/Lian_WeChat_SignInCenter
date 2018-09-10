#!/usr/bin/python
# encoding=utf-8

from tornado.web import RequestHandler, StaticFileHandler

import json

class BaseHandler(RequestHandler):
    """"自定义基类"""

    def initialize(self):
        self.add_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        print "\n"

    def prepare(self):
        """预解析json数据"""
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}

    def post(self):
        self.write('some post')

    def get(self):
        self.write('some get')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    @property
    def db(self):
        """作为RequestHandler对象的db属性"""
        return self.application.db

# class StaticFileBaseHandler(StaticFileHandler):
#     """自定义静态文件处理类, 在用户获取html页面的时候设置_xsrf的cookie"""
#     def __init__(self, *args, **kwargs):
#         super(StaticFileBaseHandler, self).__init__(*args, **kwargs)
#         self.xsrf_token