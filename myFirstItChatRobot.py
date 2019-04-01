# coding=utf-8
# 参考文档: https://segmentfault.com/a/1190000009420701
#          https://mp.weixin.qq.com/s/p5I6zimaBY8DqI2xW3WBNQ

import itchat, time, re, json, random, requests, os
from itchat.content import *
from languageLibrary import *
from Translate import *
from voiceRecognition import *

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

        # 临时新加，之后删
        if re.search('在吗', messages) or re.search('在么', messages) or re.search('在嘛', messages):
            itchat.send("你好呀，我是田a的影分身，他还在实验室疯狂科研，稍后回复你哦，\n\
我新加了识别语音的功能，可以识别普通话并将你说的话转成文字，但是翻译的不是很准确，没准会翻译成什么看不懂的奇怪的话，\
如果想试的话可以试一下哈哈。另外如果你发”工作“”学习“之类的词会有惊喜哦\n————来自田a",msg['FromUserName'])


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

@itchat.msg_register(itchat.content.RECORDING)
def voice_reply(msg):
    filename = msg['FileName']
    new_filename = filename.split('.')[0] + ".wav"
    msg['Text'](filename) # 下载MP3
    output = os.popen("lame --decode {0} {1} -h".format(filename, new_filename)) # 转换格式
    time.sleep(2) # 等待格式转换
    # os.popen("sox {0} -r 16000 {1}".format(new_filename, new_filename))
    # time.sleep(1)
    voice_text = wave2text(new_filename).rstrip(',').strip()
    defaultReply = u'我听不清你在说什么啊○△○||'
    if not voice_text:
        itchat.send(defaultReply, msg['FromUserName'])
    else:
        itchat.send(voice_text, msg['FromUserName'])

# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def download_files(msg):
#     msg.download(msg.fileName)
#     typeSymbol = {
#         PICTURE: 'img',
#         VIDEO: 'vid', }.get(msg.type, 'fil')
#     return '@%s@%s' % (typeSymbol, msg.fileName)

def main():
    itchat.auto_login(True)
    itchat.run(True)

if __name__ == "__main__":
    main()