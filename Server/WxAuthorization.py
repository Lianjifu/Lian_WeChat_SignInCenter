#!/usr/bin/python
# encoding=utf-8


import json
import urllib2

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


from Server.WxConfig import WxCofing

class WxLogin:
    def __init__(self):
        self.AppID = WxCofing.AppID
        self.AppSecret = WxCofing.AppSecret
        self.access_url = WxCofing.access_url
        self.refresh_access_url = WxCofing.refresh_access_url
        self.verify_url = WxCofing.verify_url
        self.user_message_url = WxCofing.user_message_url

    def request_url(self, url):
        try:
            result = urllib2.urlopen(url).read()
            return result
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            print str(e)

    def get_access_token(self, code):
        user_code = code
        get_access_url = self.access_url.format(self.AppID, self.AppSecret, user_code)
        resp = self.request_url(get_access_url)
        resp_data = json.loads(resp)
        if resp_data.get("errcode"):
            print "error"

        if resp_data.get("access_token"):
            access_token = resp_data.get("access_token")
            openid = resp_data.get("openid")
            # refresh_token = resp_data.get("refresh_token")
            # return access_token, openid, refresh_token
            return access_token, openid

    # def refresh_access_token(self, code):
    #     data = self.get_access_token(code)
    #     refresh_token = data[2]
    #     print "refresh_token:", refresh_token
    #     new_access_url = self.refresh_access_url % (self.AppID, refresh_token)
    #     resp = self.request_url(new_access_url)
    #     resp_data = json.loads(resp)
    #     if resp_data.get("errcode"):
    #         print "error"
    #     if resp_data.get("access_token"):
    #         access_token = resp_data.get("access_token")
    #         openid = resp_data.get("openid")
    #         return access_token, openid
    #
    # def verify_access_token(self, code):  # 验证access_token是否有效
    #     data = self.refresh_access_token(code)
    #     access_token = data[0]
    #     openid = data[1]
    #     verify_url = self.verify_url % (access_token, openid)
    #     resp = self.request_url(verify_url)
    #     resp_data = json.loads(resp)
    #     if resp_data.get("errcode") == 0:
    #         print "verify_access_token：：：", access_token, openid
    #         return access_token, openid
    #     else:
    #         return None

    def get_message(self,code):  # 4 第四步：拉取用户信息(需scope为 snsapi_userinfo)
        # data = self.verify_access_token(code)
        data = self.get_access_token(code)
        if data is None:
            return  None
        else:
            access_token = data[0]
            openid = data[1]
            user_message_url = self.user_message_url.format(access_token, openid)
            user_message = self.request_url(user_message_url)
            resp_data = json.loads(user_message)
            openid = resp_data.get("openid")  # 用户的唯一标识
            nickname = resp_data.get("nickname") # 用户昵称
            sex = resp_data.get("sex")          # 用户性别，值为1时是男性，值为2时是女性，值为0时未知
            province = resp_data.get("province")  # 省份
            city = resp_data.get("city")    # 城市
            country = resp_data.get("country")  # 国家
            headimgurl = resp_data.get("headimgurl")  # 用户头像
            print "用户信息：：：",openid, nickname, sex, province, city, country, headimgurl
            return openid, nickname, sex, province, city, country, headimgurl,


