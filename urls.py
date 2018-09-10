#!/usr/bin/python
# encoding=utf-8
# from tornado.web import StaticFileHandler
# import os

from handlers.SignHandler import JsApiSign, ScenicIndex, ScenicSign,ScenicDetails,SignResult,SignComplete, OrderHandler
from handlers.FaceMergeHandler import FaceMerge
urlpatterns = [
    (r"/api/wxsign/jsapisign", JsApiSign),
    (r"/api/wxsign/scenic/index", ScenicIndex),
    (r"/api/wxsign/scenic/sign", ScenicSign),
    (r"/api/wxsign/scenic/details", ScenicDetails),
    (r"/api/wxsign/sign/result", SignResult),
    (r"/api/wxsign/sign/complete", SignComplete),
    (r"/api/wxsign/order", OrderHandler),
    (r"/api/face/facemerge", FaceMerge),

   ]