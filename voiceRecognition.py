# coding=utf-8

import requests, json, uuid, base64, wave, os
from secrets import *

# ACCESS_TOKEN = None

# 发送APIKEY和SECRETKEY，获取token
def get_token():
    urlToken = "https://openapi.baidu.com/oauth/2.0/token"
    grant_type = "client_credentials"          
    data = {'grant_type': 'client_credentials', 
            'client_id': APIKEY, # 自己申请的应用
            'client_secret': SECRETKEY} # 自己申请的应用
    r = requests.post(urlToken, data=data)
    token = json.loads(r.text).get("access_token")
    return token

# 通过get_token()获取的token，通过post，发送相关的语音识别信息到api，获取识别结果
def wave2text(filename):
    token = get_token()
    with open(filename, "rb") as f:
        signal = f.read()
    rate = 8000
    urlVopApi = "http://vop.baidu.com/server_api"
    speech_length = len(signal)
    speech = base64.b64encode(signal).decode("utf-8")
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    rate = rate
    dev_pid_list = [1536, 1537, 1737, 1637, 1837, 1936]  # 详情见百度语音平台官网说明：https://cloud.baidu.com/doc/SPEECH/ASR-API.html
    data = {
        "format": "wav",  # 必填    格式，支持pcm、wav、amr，不区分大小写。推荐pcm
        "dev_pid": dev_pid_list[1],  # 选填	不填写lan参数生效，都不填写，默认1537（普通话 输入法模型 有标点），这里使用1537
        "token": token,  # 必填	get_token()中获取到的token
        "len": speech_length,  # 选填	本地语音文件的的字节数，单位字节
        "rate": rate,  # 必填	采样率，16000，固定值
        "speech": speech,  # 选填	本地语音文件的的二进制语音数据 ，需要进行base64 编码。与len参数连一起使用。
        "cuid": mac_address,  # 必填	用户唯一标识，用来区分用户，计算UV值。此处填写的本机mac地址
        "channel": 1}  # 必填	声道数，仅支持单声道，请填写固定值 1
    data_length = len(json.dumps(data).encode("utf-8"))
    headers = {"Content-Type": "application/json"}
    r = requests.post(urlVopApi, data=json.dumps(data), headers=headers)
    req_msg = json.loads(r.text)
    os.popen("rm *.mp3 {0}".format(filename))
    if req_msg["err_msg"] == 'success.':
        return req_msg["result"][0]
    else:
        return "抱歉，无法识别"

if __name__ == "__main__":
    filename = "16k.wav"
    result =  wave2text(filename)
    print("识别结果是：%s" %result)
