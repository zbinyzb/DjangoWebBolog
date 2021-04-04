from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import json

#全局变量,实现聊天记录以缓存的形式存在，即为阅后即焚的状态
userlist = []

class ChatConsumer(WebsocketConsumer):
    # 当信息打开时
    def connect(self):
        self.room_name = 'chatRoom' #设置聊天室
        self.room_group_name = 'zbinweb' #Group组名为zbinweb

        # Join room gruop
        #使用异步到同步方法，启动channel通道层，添加Group组
        async_to_sync(self.channel_layer.group_add)(self.room_group_name,self.channel_name)
        #允许
        self.accept()

    #当信息销毁时
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.gruop_discard)(self.room_group_name,self.channel_name)
        pass

    #当信息接收时    
    def receive(self, text_data):
        # 用json模块去读取传递进来的text_data转换成字典
        text_data_json = json.loads(text_data)
        print(text_data_json)
        # message = text_data_json['message']
        message = chat_code_to_msg(text_data_json['code'],text_data_json['msg'])

        # self.send(text_data=json.dumps(message))
        event = {
            'type': 'chat_message',
            'message' :message
        }
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,event)

    def chat_message(self,event):
        message = event['message']
        self.send(text_data=json.dumps(message))
#业务逻辑
def chat_code_to_msg(code,msg):
    global userlist
    # 对操作行为类别标志code分类处理
    #进入
    if code == 100:
        user = Token.objects.get(key=msg).user

        user_item = {
            'id':user.id,
            'username':user.username
        }

        if user_item not in userlist:
            userlist.append(user_item)
        
        res = {
            'code':100,
            'userlist':userlist
        }
    #退出
    if code == 888:
        user = Token.objects.get(key=msg).user

        user_item = {
            'id':user.id,
            'username':user.username
        }

        if user_item in userlist:
            userlist.remove(user_item)
        
        res = {
            'code':888,
            'userlist':userlist
        }
    #发送聊天内容
    if code == 200:
        user = Token.objects.get(key=msg['token']).user
        res = {
            'code':200,
            'msg':{
                'username':user.username,
                'text':msg['text']
            }
        }
    return res
        