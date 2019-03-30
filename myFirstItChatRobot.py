# coding=utf-8
# 参考文档: https://segmentfault.com/a/1190000009420701
#          https://mp.weixin.qq.com/s/p5I6zimaBY8DqI2xW3WBNQ

import itchat, time, re, json, random, requests
from itchat.content import *
from languageLibrary import *
from Translate import *

AUTOSWITCH = True # 全局开关

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isFriendChat=True)
def text_reply(msg):
    
    switchOnAndOff(msg)
    if not AUTOSWITCH:
        # print('hello1')
        return
    # print(msg)
    if msg['ToUserName'] != 'filehelper':
        # print("hello2")
        # if msg['User']['NickName'] == '田a':
        print('Message from: %s' % msg['User']['NickName'])  # 在终端上打印发送者昵称
        username = msg['User']['NickName']
        messages = msg['Text']  # 消息
        # 发送者的昵称
        # username = msg['ActualNickName']
        # print('Who sent it: %s' % username)
        # 欢迎
        if re.search('你好', messages) or re.search('hello', messages) or re.search('hi', messages) or re.search('田阿', messages):
            itchat.send(HELLO['hello'],msg['FromUserName'])
        # 汉译英和英译汉，带有+_+前缀为汉译英，带有=_=前缀为英译汉
        if re.search('翻译', messages):
            itchat.send('只要在你要翻译的内容前加上+_+就可以翻译咯', msg['FromUserName'])

        if messages.strip()[:3] == '+_+':
            ori_msg,zh_msg = youdao_trans(messages[3:], 1)
            itchat.send(zh_msg, msg['FromUserName'])
        match = re.search(u'工作', messages) or re.search(u'加班', messages)
        if match:
            print('-+-+' * 5)
            print('Message content:%s' % msg['Content'])
            print('工作、加班 is: %s' % (match is not None))
            randomIdx = random.randint(0, len(REPLY['工作']) - 1)
            itchat.send('%s\n%s' % (username, REPLY['工作'][randomIdx]), msg['FromUserName'])
        match = re.search('学习', messages) or re.search('考试', messages)
        if match:
            print('-+-+' * 5)
            print('Message content:%s' % msg['Content'])
            print('学习、考试 is: %s' % (match is not None))
            randomIdx = random.randint(0, len(REPLY['学习']) - 1)
            itchat.send('%s\n%s' % (username, REPLY['学习'][randomIdx]), msg['FromUserName'])
        # print('isAt is:%s' % msg['isAt'])
        # if msg['isAt']:
        #     randomIdx = random.randint(0, len(REPLY['default']) - 1)
        #     itchat.send('%s\n%s' % (username, REPLY['default'][randomIdx]), msg['FromUserName'])
        #     print('-+-+'*5)

        # msg.user.send('%s: %s' % (msg.type, msg.text))

def switchOnAndOff(msg):
  global AUTOSWITCH
  if msg['ToUserName'] == 'filehelper':
    if msg['Text'] == '启动托管':
      AUTOSWITCH = True
      itchat.send('托管中', toUserName='filehelper')
    elif msg['Text'] == '取消托管':
      AUTOSWITCH = False
      itchat.send( 'OK', toUserName='filehelper')
    elif msg['Text'] == '托管状态':
      itchat.send(AUTOREPLYSTATUS[AUTOSWITCH], toUserName='filehelper')

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

def main():
    itchat.auto_login(True)
    itchat.run(True)

if __name__ == "__main__":
    main()