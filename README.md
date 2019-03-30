# MyITChatRobot
通过python的itChat库制作一个简单的可自动回复的机器人儿。<br>
## python库：itChat
介绍：登录微信，将收发信息统一打包为字典（dict）形式，然后使用post请求进行信息交换。就是一个可编写脚本控制、无界面的网页版微信客户端。<br>
## itchat库如何安装
首先确保电脑上已安装python<br>
然后pip安装：pip install -i https://pypi.douban.com/simple <br>
## 准备实现的功能
首先考虑基于个人的，之后有缘再更新有关群消息回复的<br>
其实就是一个参数的事，在注册时（@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True,isMpChat=True)）想要哪个参数直接赋值为True即可，分别表示：<br>
isFriendChat -- 来自好友的信息<br>
isGroupChat -- 来自群消息<br>
isMpChat -- 来自公众号消息<br>
## 目前进度：2/100
1. 实现中英自动翻译：<br>
当接收到的消息的以+_+开头，则自动识别语言翻译。<br>
2. 实现 ** 托管 ** 功能：<br>
向【文件传输助手】发送“取消托管”，可取消自动回复功能，发送“托管”则恢复自动回复功能，发送“托管状态”显示是否在托管中。<br>
3. 准备实现语音/视频识别和转文字格式功能。【有缘再更新。。。】<br>