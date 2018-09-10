# encoding=utf-8
class RET:
    OK = "20000"
    ERROR = "40000"
    DBERR = "40001"
    NODATA = "40002"
    DATAEXIST = "40003"
    DATAERR = "40004"
    PARAMERR = "40005"
    SERVERERR = "45000"
    UNKOWNERR = "45010"



error_map = {
    RET.OK: u"成功",
    RET.ERROR : u"失败",
    RET.DBERR: u"数据库查询错误",
    RET.NODATA: u"无数据",
    RET.DATAEXIST: u"数据已存在",
    RET.DATAERR: u"数据错误",
    RET.PARAMERR : u"参数错误",
    RET.SERVERERR: u"内部错误",
    RET.UNKOWNERR: u"未知错误",

}
