# coding=utf-8

import requests, json, uuid, base64, wave
from secrets import *

ACCESS_TOKEN = None

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
    global ACCESS_TOKEN
    try:
        filename = open(filename, 'rb')
    except IOError:
        print(u'文件错误~')
        return

    filename   = wave.open(filename)
    n_frames   = filename.getnframes()
    print(n_frames)
    frame_rate = filename.getframerate()
    if n_frames == 1 or frame_rate not in (8000, 16000):
        print(u'不符合格式')
        return
    audio   = filename.readframes(n_frames)
    seconds = n_frames/frame_rate + 1
    minute  = seconds/60 + 1
    for i in range(0, minute):
        sub_audio    = audio[i*60*frame_rate:(i+1)*60*frame_rate]
        base_data    = base64.b64encode(sub_audio)
        access_token = ACCESS_TOKEN or get_token()


    urlVopApi = "http://vop.baidu.com/server_api"
    # speech_length = len(sig)
    # speech = base64.b64encode(sig).decode("utf-8")
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    # rate = rate
    data = {
        "format": "wav",
        "lan": "zh",
        "token": access_token,
        "len": len(sub_audio),
        "rate": frame_rate,
        "speech": base_data,
        "cuid": mac_address,
        "channel": 1}
    # data_length = len(json.dumps(data).encode("utf-8"))
    # headers = {"Content-Type": "application/json"}
    r = requests.post(urlVopApi, json.dumps(data), {"Content-Type": "application/json"})
    print(r.text)

if __name__ == "__main__":
    filename = "hello.wav"

    # signal = open(filename, "rb").read()
    # rate = 8000
    
    token = get_token()
    # print(signal)
    # wave2text(signal, rate, token)
    wave2text(filename)