#!/usr/bin/python
# encoding=utf-8

import datetime
import json
import urllib
from Server.WxConfig import WxCofing
import uuid
import time
from hashlib import sha1
import ast
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class JsTicket:
    _access_token = {
        'token': '',
        'updatetime': datetime.datetime.now(),
        'expires_in': ''
    }

    _js_ticket = {
        'ticket': '',
        'updatetime': datetime.datetime.now(),
        'expires_in': ''
    }

    @classmethod
    def get_access_token(cls):
        # 如果access_token不存在，或是有效期已过，调用update_access_token方法，生成access_token
        if not cls._access_token['token'] or (
                    datetime.datetime.now() - cls._access_token['updatetime']).seconds >= 6800:
            return cls._update_access_token()
        else:
            return cls._access_token['token']

    @classmethod
    def _update_access_token(cls):
        # 构造请求的url，把appid和appsecret添加到url
        url = WxCofing.get_access_url
        # 获取响应数据
        resp = urllib.urlopen(url).read()
        resp_data = json.loads(resp)
        cls._access_token['token'] = resp_data.get('access_token')
        return cls._access_token['token']

    @classmethod
    def get_js_ticket(cls):
        if not cls._js_ticket['ticket'] or (
                    datetime.datetime.now() - cls._js_ticket['updatetime']).seconds >= 6800:
            return cls._update_js_ticket()
        else:
            return cls._js_ticket['ticket']

    @classmethod
    def _update_js_ticket(cls):
        ticket = cls.get_access_token()
        url = WxCofing.get_ticket_url.format(ticket)

        resp = urllib.urlopen(url).read()
        resp_data = ast.literal_eval(resp)
        cls._js_ticket['ticket'] = resp_data.get('ticket')
        return cls._js_ticket['ticket']


class JsapiSign:
    def __init__(self):
        self.jsapi_ticket = JsTicket.get_js_ticket()
        self.url = WxCofing.AppHost

    def create_noncestr(self):
        return ''.join(str(uuid.uuid4()).split('-'))[0:16]

    def create_timestamp(self):
        timestamp = int(time.time())
        return str(timestamp)

    def sign(self, js_url):
        jsapi_ticket = self.jsapi_ticket
        url = js_url
        noncestr = self.create_noncestr()
        timestamp = self.create_timestamp()
        if url is not None and jsapi_ticket is not None and noncestr is not None and timestamp is not None:
            string = "jsapi_ticket=" + jsapi_ticket + "&noncestr=" + noncestr + "&timestamp=" + timestamp + "&url=" + url
            signature = sha1(string)
            return noncestr, timestamp, signature
        else:
            return None
