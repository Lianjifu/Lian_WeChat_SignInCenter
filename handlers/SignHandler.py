#!/usr/bin/python
# encoding=utf-8

from BaseHandler import BaseHandler
from Server.WxAuthorization import WxLogin
from utilities.utils import *
from utilities.response_code import RET
from utilities.db_util import db_util
import logging
from Server.WxJsSign import JsapiSign
import datetime
import time


# 基础配置
class JsApiSign(BaseHandler):
    def post(self):
        """基础的配置参数"""
        api_log_start("WxConfig")
        ExpectParams = ["wx_user_code", "wx_url"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write(dict(code=RET.PARAMERR, msg="params error"))
        wx_user_code = str(RqstDt.get('wx_user_code'))
        wx_url = str(RqstDt.get('wx_url'))
        user_data = WxLogin().get_message(wx_user_code)
        sign_data = JsapiSign().sign(wx_url)
        if user_data is None or sign_data is None:
            return self.write(dict(code=RET.ERROR, msg="user_data or sign_data ERROR"))
        else:
            noncestr = sign_data[0]
            timestamp = sign_data[1]
            signature = sign_data[2].hexdigest()
            wx_user_openid = user_data[0]
            wx_user_nickname = user_data[1]
            wx_user_sex = user_data[2]
            wx_user_province = user_data[3]
            wx_user_city = user_data[4]
            wx_user_country = user_data[5]
            wx_user_headimgurl = user_data[6]
            sign_d = {
                "noncestr": noncestr,
                "timestamp": timestamp,
                "signature": signature,
            }
            conf_data = {
                "wx_user_openid": wx_user_openid,
                "wx_user_nickname":wx_user_nickname ,
                "wx_user_sex": wx_user_sex,
                "wx_user_province": wx_user_province,
                "wx_user_city": wx_user_city,
                "wx_user_country": wx_user_country,
                "wx_user_headimgurl": wx_user_headimgurl,
                "wx_sign": sign_d
            }
            return self.write(dict(code=RET.OK, msg="OK", data=conf_data))

# 景区首页
class ScenicIndex(BaseHandler):
    def post(self):
        # 根据签到者位置的纬度与经度进行推荐最近的景区
        api_log_start("ScenicIndex")
        index_data = []
        ExpectParams = ['wx_user_openid', 'wx_user_longitude', 'wx_user_latitude']
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write(dict(code=RET.PARAMERR, msg="params error"))
        wx_user_openid = str(RqstDt.get('wx_user_openid'))
        wx_user_longitude = str(RqstDt.get('wx_user_longitude'))
        wx_user_latitude = str(RqstDt.get('wx_user_latitude'))
        if wx_user_longitude is None and wx_user_latitude is None:
            try:
                DbInit1 = db_util()
                _sql = "SELECT wx_scenic_id, wx_scenic_name,wx_scenic_image FROM ywgsh_wxsign_scenic_info LIMIT 10"
                results = DbInit1.selectSQL(_sql, _type="all")
                if results:
                    for row in results:
                        d = {
                            "wx_scenic_id": row["wx_scenic_id"],
                            "wx_scenic_name": row["wx_scenic_name"],
                            "wx_scenic_image": row["wx_scenic_image"],
                        }
                        index_data.append(d)
                    DbInit1.close()
                else:
                    return self.write(dict(code=RET.NODATA, msg="no data"))
            except Exception as e:
                logging.error(e)
                return self.write(dict(code=RET.DBERR, msg="get date error"))
        else:
           try:
               DbInit = db_util()
               _sql = "SELECT * FROM(SELECT wx_scenic_id, wx_scenic_name, wx_scenic_image,ROUND (6378.138*2*ASIN(SQRT(POW(SIN((" + wx_user_latitude + "*PI()/180-wx_scenic_latitude*PI()/180)/2),2)+COS(" + wx_user_latitude + "*PI()/180)*COS(wx_scenic_latitude*PI()/180)*POW(SIN((" + wx_user_longitude + "*PI()/180-wx_scenic_longitude*PI()/180)/2),2)))*1000)AS distance FROM ywgsh_wxsign_scenic_info ORDER BY distance ) AS a WHERE a.distance <= 80000;"
               results = DbInit.selectSQL(_sql, _type="all")
               if results:
                   for row in results:
                       d = {
                           "wx_scenic_id": row["wx_scenic_id"],
                           "wx_scenic_name": row["wx_scenic_name"],
                           "wx_scenic_image": row["wx_scenic_image"],
                           "wx_scenic_distance": row["distance"],
                       }
                       index_data.append(d)
                   DbInit.close()
               else:
                   return self.write(dict(code=RET.NODATA, msg="no data"))
           except Exception as e:
               logging.error(e)
               return self.write(dict(code=RET.DBERR, msg="get date error"))

        return  self.write(dict(code=RET.OK, msg="OK", data=index_data))

# 签到页面
class ScenicSign(BaseHandler):
    def post(self):
        api_log_start("ScenicSign")
        sign_data = []

        ExpectParams = ["wx_user_openid"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write(dict(code=RET.PARAMERR, msg="params error"))
        wx_user_openid = str(RqstDt.get('wx_user_openid'))
        try:
            DbInit = db_util()
            _sql = 'SELECT * FROM ywgsh_wxsign_scenic_info as sce INNER JOIN ywgsh_wxsign_sign_info as sig ON sce.wx_scenic_id = sig.wx_scenics_id WHERE wx_user_openid ="%s";'%(wx_user_openid)
            print _sql
            DbRsSel = DbInit.selectSQL(_sql, _type="all")
            print "DbRsSel:::::", DbRsSel
            if DbRsSel:
                for row in DbRsSel:
                    d = {
                        "wx_scenic_id": row["wx_scenic_id"],
                        "wx_scenic_city": row["wx_scenic_city"],
                        "wx_scenic_name": row["wx_scenic_name"],
                        "wx_scenic_image": row["wx_scenic_image"],
                        "wx_sign_create_date": row["wx_sign_create_date"]
                    }
                    sign_data.append(d)
            else:
                return self.write(dict(code=RET.NODATA, msg="no data"))
            DbInit.close()
        except Exception as e:
            logging.error(e)
            return self.write(dict(code=RET.DBERR, msg="get date error"))
        return self.write(dict(code=RET.OK, msg="OK", data=sign_data))


# 景区详情页
class ScenicDetails(BaseHandler):
    def post(self):
        # 根据点击的景区的位置，分析最近景区出售纪念币的景区
        api_log_start("ScenicDetails")
        details_data = []
        ExpectParams = ["wx_user_openid", "wx_scenic_id"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write(dict(code=RET.PARAMERR, msg="params error"))
        wx_user_openid = str(RqstDt.get('wx_user_openid'))
        wx_scenic_id = str(RqstDt.get('wx_scenic_id'))

        # 查询景区的纪念币
        try:
            DbInit1 = db_util()
            _sql = 'SELECT * FROM ywgsh_wxsign_product_info WHERE wx_scenic_product_id="%s";'% (wx_scenic_id)
            print _sql
            DbRsSel = DbInit1.selectSQL(_sql, _type="all")
            print "DbRsSel:::::", DbRsSel
            details_pi_data = []
            if DbRsSel:
                for i in DbRsSel:
                    pi = {
                        "wx_product_id" : i["wx_product_id"],
                        "wx_product_name" : i["wx_product_name"],
                        "wx_product_image" : i["wx_product_image"]
                    }
                    details_pi_data.append(pi)
            DbInit1.close()
        except Exception as e:
            logging.error(e)
            return self.write({"code": RET.DBERR, "msg": "查询景区的纪念币失败"})

        # 查询周边的产品(除了本景区的纪念币外随机选择3个)
        try:
            DbInit2 = db_util()
            # _sql = 'SELECT * FROM ywgsh_wxsign_product_info WHERE wx_scenic_product_id="%s";'% (wx_scenic_id)
            _sql = 'SELECT * FROM ywgsh_wxsign_product_info AS wpi INNER JOIN ywgsh_wxsign_scenic_info AS wsi ON wpi.wx_scenic_product_id = wsi.wx_scenic_id WHERE wsi.wx_scenic_id != "%s" ORDER BY rand() LIMIT 4;'%(wx_scenic_id)
            print _sql
            DbRsSel = DbInit2.selectSQL(_sql, _type="all")
            print "DbRsSel:::::", DbRsSel
            details_around_data = []
            if DbRsSel:
                for i in DbRsSel:
                    pi = {
                        "wx_scenic_id": i["wx_scenic_product_id"],
                        "wx_product_id": i["wx_product_id"],
                        "wx_product_name": i["wx_product_name"],
                        "wx_product_image": i["wx_product_image"]
                    }
                    details_around_data.append(pi)
            DbInit2.close()
        except Exception as e:
            logging.error(e)
            return self.write({"code": RET.DBERR, "msg": "查询周边的纪念币失败"})

        # 查询轮播图
        try:
            DbInit3 = db_util()
            _sql = 'SELECT * FROM ywgsh_wxsign_slide_info WHERE wx_scenic_slide_id="%s";'%(wx_scenic_id)
            print _sql
            DbRsSel = DbInit3.selectSQL(_sql, _type="all")
            print "DbRsSel:::::", DbRsSel
            details_silde_data = []
            if DbRsSel:
                for i in DbRsSel:
                    su = {
                        "wx_scenic_slide_image": i["wx_scenic_slide_image"]
                    }
                    details_silde_data.append(su)
            DbInit3.close()
        except Exception as e:
            logging.error(e)
            return self.write({"code": RET.DBERR, "msg": "查询轮播图失败"})
        # 查询景区的信息
        try:
            DbInit4 = db_util()
            sql = 'SELECT * FROM ywgsh_wxsign_scenic_info WHERE wx_scenic_id="%s";' %(wx_scenic_id)
            print sql
            DbRsSel = DbInit4.selectSQL(sql, _type="all")
            print "DbRsSel:::::", DbRsSel
            if DbRsSel:
                for row in DbRsSel:
                    d = {
                        "wx_scenic_city": row["wx_scenic_city"],
                        "wx_scenic_name": row["wx_scenic_name"],
                        "wx_scenic_details_image": row["wx_scenic_details_image"],
                        "wx_scenic_slide_urls": details_silde_data,
                        "wx_products_info": details_pi_data,
                        "wx_products_around_info": details_around_data
                    }
                    details_data.append(d)
            else:
                return self.write(dict(code=RET.DBERR, msg="query fails"))
            DbInit4.close()
        except Exception as e:
            logging.error(e)
            return self.write({"code": RET.DBERR, "msg": "查询景区信息失败"})

        return  self.write(dict(code=RET.OK, msg="OK", data=details_data))


# 签到结果
class SignResult(BaseHandler):
    def post(self):
        api_log_start("SignResult")
        result_data = []
        result_data1 = []
        global _wx_user_openid, _wx_scenic_city, _wx_scenic_name,_wx_scenic_image
        ExpectParams = ["wx_user_openid", "wx_user_longitude", "wx_user_latitude"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write(dict(code=RET.PARAMERR, msg="params error"))
        _wx_user_openid = str(RqstDt.get('wx_user_openid'))
        wx_user_longitude = str(RqstDt.get('wx_user_longitude'))
        wx_user_latitude = str(RqstDt.get('wx_user_latitude'))
        try:
            DbInit1 = db_util()
            # SELECT * FROM(SELECT wx_scenic_id, wx_scenic_name, wx_scenic_image,wx_scenic_ranknum, ROUND (6378.138*2*ASIN(SQRT(POW(SIN((31.1504443482*PI()/180-wx_scenic_latitude*PI()/180)/2),2)+COS(31.1504443482*PI()/180)*COS(wx_scenic_latitude*PI()/180)*POW(SIN((121.6667819009*PI()/180-wx_scenic_longitude*PI()/180)/2),2)))*1000)AS distance FROM ywgsh_wxsign_scenic_info AS sce INNER JOIN ywgsh_wxsign_sign_info AS sig ON sce.wx_scenic_id = sig.wx_scenics_id ORDER BY distance ) AS a WHERE a.distance <= 80000 limit 0,1;
            sql = "SELECT * FROM(SELECT wx_scenic_id, wx_scenic_city, wx_scenic_name,wx_scenic_image,ROUND (6378.138*2*ASIN(SQRT(POW(SIN(("+wx_user_latitude+"*PI()/180-wx_scenic_latitude*PI()/180)/2),2)+COS("+wx_user_latitude+"*PI()/180)*COS(wx_scenic_latitude*PI()/180)*POW(SIN(("+wx_user_longitude+"*PI()/180-wx_scenic_longitude*PI()/180)/2),2)))*1000)AS distance FROM ywgsh_wxsign_scenic_info ORDER BY distance ) AS a WHERE a.distance <= 5000 limit 0,1;"
            print sql
            DbRsSel = DbInit1.selectSQL(sql, _type="all")
            print "DbRsSel:::::", DbRsSel
            if DbRsSel:
                for row in DbRsSel:
                    _wx_scenic_id = row["wx_scenic_id"]
                    _wx_scenic_city = row["wx_scenic_city"]
                    _wx_scenic_name = row["wx_scenic_name"]
                    _wx_scenic_image = row["wx_scenic_image"]
            else:
                return self.write(dict(code=RET.NODATA, msg="未查到数据"))
            DbInit1.close()
        except Exception as e:
            logging.error(e)
            return self.write(dict(code=RET.DBERR, msg="数据库异常"))
        try:
            DbInit2 = db_util()
            Sql = 'SELECT * FROM ywgsh_wxsign_sign_info WHERE wx_user_openid="%s" AND wx_scenics_id="%s";'% (_wx_user_openid,_wx_scenic_id)
            DbRsSel = DbInit2.selectSQL(Sql, _type="all")
            if DbRsSel:
                d = {
                    "wx_scenic_id": _wx_scenic_id,
                    "wx_scenic_city": _wx_scenic_city,
                    "wx_scenic_name": _wx_scenic_name,
                    "wx_scenic_image": _wx_scenic_image
                }
                result_data1.append(d)
                DbInit2.close()
                return self.write(dict(code=RET.DATAEXIST, msg="DATAEXIST",data= result_data1))
            else:
                timestamp = int(time.time())
                DbInit3 = db_util()
                _sql = 'INSERT INTO ywgsh_wxsign_sign_info(wx_user_openid,wx_scenics_id,wx_sign_create_date)VALUES (%s,%s,%s)'
                DbRsIn = DbInit3.executeSQL(_sql, (_wx_user_openid, _wx_scenic_id, timestamp))
                if DbRsIn:
                    DbInit3.commit()
                    d = {
                        "wx_scenic_id" : _wx_scenic_id,
                        "wx_sign_create_date": timestamp,
                        "wx_scenic_city": _wx_scenic_city,
                        "wx_scenic_name": _wx_scenic_name,
                        "wx_scenic_image": _wx_scenic_image
                    }
                    result_data.append(d)
                    DbInit3.close()
                else:
                    DbInit3.close()
                    return self.write(dict(code=RET.ERROR, msg="error"))
                DbInit2.close()
        except Exception as e:
            logging.error(e)
            return self.write(dict(code=RET.DBERR, msg="DBERR"))

        return self.write(dict(code=RET.OK, msg="OK", data=result_data))

# 6个签到完成
class SignComplete(BaseHandler):
    def post(self):
        api_log_start("SignComplete")
        complete_data = []
        try:
            DbInit = db_util()
            _sql = 'SELECT * FROM ywgsh_wxsign_souvenir_info'
            print _sql
            DbRsSel = DbInit.selectSQL(_sql, _type="all")
            print "DbRsSel:::::", DbRsSel
            if DbRsSel:
                for row in DbRsSel:
                    d = {
                        "wx_souvenir_medal_id": row["wx_souvenir_medal_id"],
                        "wx_souvenir_medal_name": row["wx_souvenir_medal_name"],
                        "wx_souvenir_medal_style": row["wx_souvenir_medal_style"],
                        "wx_souvenir_medal_color": row["wx_souvenir_medal_color"],
                        "wx_souvenir_medal_price": row["wx_souvenir_medal_price"],
                        "wx_souvenir_medal_num": row["wx_souvenir_medal_num"],
                        "wx_souvenir_medal_image": row["wx_souvenir_medal_image"],
                    }
                    complete_data.append(d)
            else:
                return self.write(dict(code=RET.NODATA, msg="no data"))
            DbInit.close()
        except Exception as e:
            logging.error(e)
            return self.write(dict(code=RET.DBERR, msg="get date error"))

        return self.write(dict(code=RET.OK, msg="OK", data=complete_data))

# 订单
class OrderHandler(BaseHandler):
    def post(self):
        api_log_start("OrderHandler")
        ExpectParams = ["wx_user_openid", "wx_user_name", "wx_user_phone_number", "wx_user_address"]
        RqstDt = verify_request_body(self, ExpectParams)
        # 校验参数
        if not RqstDt:
            return self.write(dict(code=RET.PARAMERR, msg="params error"))
        wx_user_openid = str(RqstDt.get('wx_user_openid'))
        wx_user_name = str(RqstDt.get('wx_user_name'))
        wx_user_phone_number = str(RqstDt.get('wx_user_phone_number'))
        wx_user_address = str(RqstDt.get('wx_user_address'))
        wx_order_date = datetime.datetime.now()

        try:
            DbInit = db_util()
            _sql = 'INSERT INTO ywgsh_wxsign_order_info(wx_user_openid,wx_user_name,wx_user_phone_number,wx_user_address,wx_order_date)VALUES (%s, %s, %s, %s, %s)'
            print _sql

            DbRsIns = DbInit.executeSQL(_sql, (
                wx_user_openid, wx_user_name, wx_user_phone_number, wx_user_address, wx_order_date))
            if DbRsIns:
                DbInit.commit()
            else:
                return self.write(dict(code=RET.ERROR, msg="error"))
            DbInit.close()
        except Exception as e:
            logging.error(e)
            return self.write(dict(code=RET.DBERR, msg="get date error"))

        return self.write(dict(code=RET.OK, msg="OK"))
