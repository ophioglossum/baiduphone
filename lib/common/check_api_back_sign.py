from lib.common import rsa,logrecord
from config import app
#接口返回验证签名
def checkDataSign(data):
    buff = []
    for k in data:
        if k != "sign" and data[k] != "" and not (isinstance(data[k],dict) or isinstance(data[k],list)):
            buff.append(f'{k}={data[k]}')
    sbuff=sorted(buff)
    tmpStr = '&'.join(sbuff)
    stringSignTemp = f'{tmpStr}&key={app.MD5_KEY}'
    logrecord.log(f"签名的数据包:{stringSignTemp}")
    sign = rsa.EnMd5(stringSignTemp).upper()
    logrecord.log(f"验证的签名包:{sign}")
    logrecord.log(f"接口返回的签名包:{data['sign']}")
    return data['sign']==sign