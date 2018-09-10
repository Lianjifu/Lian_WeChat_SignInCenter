#!/usr/bin/python
# encoding=utf-8

from BaseHandler import BaseHandler
from utilities.utils import *
from utilities.response_code import RET
from Server.WxFaceMerge import WxFace
import base64
import json


# 人脸融合API
class FaceMerge(BaseHandler):
    def post(self):
        api_log_start("FaceMerge")
        ExpectParams = ["wx_face_image", "wx_face_model"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write(dict(code=RET.PARAMERR, msg="params error"))
        wx_face_image = str(RqstDt.get('wx_face_image'))
        wx_face_model = str(RqstDt.get('wx_face_model'))
        face_data = WxFace().request_url(wx_face_image, wx_face_model)
        res_ret = face_data.json()["ret"]
        if res_ret == 0:
            res_image = base64.b64decode(face_data.json()['data']['image'])
            return self.write(dict(code=RET.OK, msg="OK", data=res_image))
        elif res_ret == 16396:
            return self.write(dict(code=16396, msg="图片格式非法"))
        elif res_ret == 16397:
            return self.write(dict(code=16397, msg="图片体积过大"))
        elif res_ret == 16402:
            return self.write(dict(code=16402, msg="图片没有人脸"))
        elif res_ret == 16415:
            return self.write(dict(code=16402, msg="图片为空"))
        else:
            return self.write(dict(code=RET.ERROR, msg="error"))