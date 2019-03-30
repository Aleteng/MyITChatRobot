# coding=utf-8
# 参考文档: https://segmentfault.com/a/1190000009420701
#          https://mp.weixin.qq.com/s/p5I6zimaBY8DqI2xW3WBNQ

import itchat, time, re, json, random
from itchat.content import *
from languageLibrary import *

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    # print(msg)
    if msg['User']['NickName'] == u'田a':
        print('Message from: %s' % msg['User']['NickName'])  # 在终端上打印发送者昵称
        # 发送者的昵称
        # username = msg['ActualNickName']
        # print('Who sent it: %s' % username)

        match = re.search(u'工作', msg['Text']) or re.search(u'加班', msg['Text'])
        if match:
            print('-+-+' * 5)
            print('Message content:%s' % msg['Content'])
            print('工作、加班 is: %s' % (match is not None))
            randomIdx = random.randint(0, len(REPLY['工作']) - 1)
            itchat.send('%s\n%s' % (username, REPLY['工作'][randomIdx]), msg['FromUserName'])

        match = re.search('学习', msg['Text']) or re.search('考试', msg['Text'])
        if match:
            print('-+-+' * 5)
            print('Message content:%s' % msg['Content'])
            print('学习、考试 is: %s' % (match is not None))
            randomIdx = random.randint(0, len(REPLY['学习']) - 1)
            itchat.send('%s\n%s' % (username, REPLY['学习'][randomIdx]), msg['FromUserName'])

        print('isAt is:%s' % msg['isAt'])

        if msg['isAt']:
            randomIdx = random.randint(0, len(REPLY['default']) - 1)
            itchat.send('%s\n%s' % (username, REPLY['default'][randomIdx]), msg['FromUserName'])
            print('-+-+'*5)

    msg.user.send('%s: %s' % (msg.type, msg.text))

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

itchat.auto_login(True)
itchat.run(True)

