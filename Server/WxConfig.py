#!/usr/bin/python
# encoding=utf-8


class WxCofing(object):
    """微信开发--基础配置"""

    AppID = ""
    AppSecret = ""

    # 微信网页开发域名
    AppHost = ""

    redirect_uri = ""

    code_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_userinfo&state=STATE&connect_redirect=1#wechat_redirect".format(AppID,redirect_uri)

    access_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code"

    refresh_access_url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=%s&grant_type=refresh_token&refresh_token=%s'

    verify_url = "https://api.weixin.qq.com/sns/auth?access_token=%s&openid=%s"

    user_message_url = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'

    get_access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
        AppID, AppSecret)

    get_ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi"


    # 人脸融合需要的配置参数
    ai_qq_app_id = "002108333085"

    ai_qq_app_key = "--p83Xxe9qcfUkYndF-"

    face_merge_url = "https://api.ai.qq.com/fcgi-bin/ptu/ptu_facemerge"
