#!/usr/bin/python
# encoding=utf-8

import requests
import time
import hashlib
import base64
import uuid
from urllib import urlencode
from Server.WxConfig import WxCofing


class WxFace:
    def __init__(self):
        self.face_merge_url = WxCofing.face_merge_url      # 人脸融合接口
        self.ai_qq_app_key = WxCofing.ai_qq_app_key        # 腾讯AI开放平台应用key
        self.ai_qq_app_id = WxCofing.ai_qq_app_id          # 腾讯AI开放平台应用id

    # 腾讯AI开放平台-Facemerge接口鉴权签名
    def get_sign(self, para):
        # 签名的key有严格要求，按照key升序排列
        data = sorted(para.items(), key=lambda item: item[0])
        s = urlencode(data)
        # app_key最后加
        s += '&app_key=' + self.ai_qq_app_key
        # 计算md5报文信息
        md5 = hashlib.md5()
        md5.update(s)
        digest = md5.hexdigest()
        return digest.upper()

    # 读取图片数据
    def read_image(self, image):
        raw_data = open(image, "rb").read()
        image_data = base64.b64encode(raw_data)
        return image_data

    # 生成随机字符串16位
    def nonce_str(self):
        nonce_str = ''.join(str(uuid.uuid4()).split('-'))[0:16]
        return nonce_str

    # 发送post数据
    def request_url(self, image, model):
        image_data = self.read_image(image)
        nonce_str = self.nonce_str()
        data = {
            'app_id': self.ai_qq_app_id,
            'image': image_data,
            'model': model,  # 选定想要融合的模板
            'time_stamp': str(int(time.time())),
            'nonce_str': nonce_str,
        }
        data["sign"] = self.get_sign(data)
        res = requests.post(self.face_merge_url, data=data)
        return res




