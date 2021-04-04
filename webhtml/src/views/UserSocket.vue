<template>
    <div id="user-socket" class="body">
        <el-row :gutter="10">
            <el-col :span="6">
                <div class="dweb">
                    <div class="header">
                        在线群友
                    </div>
                    <el-divider></el-divider>
                    <el-row :gutter="10"> 
                        <el-col v-for="item in userlist" :key="item.id" :span="24">
                            <div class="dweb">
                                <div class="userlist-item">
                                    <span>{{ item.username }}</span>
                                </div>
                            </div>
                        </el-col>
                    </el-row>
                </div>
            </el-col>
            <el-col :span="18">
                <div class="dweb">
                    <div class="header">
                        聊天室
                    </div>
                    <el-divider></el-divider>
                    <div id="msg-box">
                        <div v-for="(item,index) in message_list" :key="index" class="textother">
                            <div class="username">{{ item.username }}</div>
                            <div class="text">{{ item.text }}</div>
                        </div>
                    </div>
                    <div id="input-send">
                        <el-input @keyup.enter="sendMessage" type="textarea" :rows="3" placeholder="请输入内容" v-model="sendmsg">
                        </el-input>
                        <el-button @click="sendMessage" type="success">发送信息</el-button>
                    </div>
                </div>
            </el-col>
        </el-row>   
    </div>
</template>

<script>
export default {
    data() {
        return {
            sendmsg:"",//发送信息
            userlist:[],//用户列表
            message_list:[]//每条信息
        }
    },
    //在组件销毁前
    beforeDestroy() {
        let leaveRoom = {
            code: 888,
            msg:this.$store.getters.isnotUserlogin
        }
        this.sendWebSocketMsg(leaveRoom)
    },
    mounted() {
        this.initWebSocket();
    },
    methods:{
        //初始化
        initWebSocket(){
            //初始化websocket
                //连接服务端,开启一个新的websocket
            this.websock = new WebSocket("ws://127.0.0.1:9000/chat-channel/");
            //指定事件回调
            this.websock.onopen = this.websocketOnOpen;
            this.websock.onmessage = this.websocketOnMessage;
            this.websock.onerror = this.websocketOnError;
            this.websock.onclose = this.websocketClose;            
        },
        //发送聊天信息
        sendMessage(){
            let textmsg = {
                code:200,
                msg:{
                    token:this.$store.getters.isnotUserlogin,
                    text:this.sendmsg
                }
            }
            this.sendWebSocketMsg(textmsg)
        },
        //发送消息
        sendWebSocketMsg(msg){
            //由于js的对象是传不出去的，需要先转成json类型的字符串
            this.websock.send(JSON.stringify(msg))
        },
        websocketOnOpen(e){
            console.log(e);
            let token = this.$store.getters.isnotUserlogin
            let enterroom = {
                code:100,
                msg:token
            }
            this.sendWebSocketMsg(enterroom)
        },
        websocketOnMessage(e){
            // //获取字符串
            // console.log(e.data);
            //转换成js可处理的对象
            let message = JSON.parse(e.data)
            console.log(message)
            if(message.code == 100 || message.code == 888 ){
                console.log('进入房间 / 离开房间')
                //赋值
                this.userlist = message.userlist
            }
            if(message.code == 200){
                this.message_list.push(message.msg)
                this.$nextTick(function (){
                    let div = document.getElementById('msg-box')
                    this.sendmsg = ''
                    div.scrollTop = div.scrollHeight
                })
            }

        },
        websocketOnError(e){
            console.log(e);

        },
        websocketClose(e){
            console.log("断开连接", e.code +" "+e.reason + " " + e.wasClean);

        },
    },
}
</script>

<style scoped>
    .userlist-item{
        text-align: center;
        color: #fff;
    }
    #msg-box{
        height: 320px;
        padding: 10px 20px;
        overflow-y: scroll;
    }
    #input-send{
        display: flex;

    }
    .textother{
        background: #00000060;
        border-radius: 10px;
        color: #fff;
        width: 300px;
        padding: 10px 10px 10px 10px;
        margin-top: 10px;
    }
    .username{
        width: 100%;
        font-size: 1.3rem;
        color: #fd7e14;
    }
    .text{
        background: #00000060;
        border-radius: 10px;
        color: #fff;
        width: 100%;
        padding: 10px 10px 10px 20px;
    }
    
</style>