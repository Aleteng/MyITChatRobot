import json, requests

# 翻译 transType: 0 -- en -> zh; 1 -- zh -> en
def youdao_trans(messages, transType):
    urlYoudao = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    if transType:
        keywords = {
            'type': 'AUTO',
            'i': messages,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'ue': 'UTF-8',
            'action': 'FY_BY_CLICKBUTTON',
            'typoResult': 'true'
        }

        req = requests.post(urlYoudao, data=keywords)
        if req.status_code == 200:  # 正确响应
            result = json.loads(req.text)  # 把返回的结果加载为json格式
            print(result)
            return [result['translateResult'][0][0]['src'],result['translateResult'][0][0]['tgt']]
        else:
            print('翻译失败，请重试-_-#')
            return None