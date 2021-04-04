<template>
  <div id="app">
    <!-- 返回顶部 -->
    <el-backtop>
    <div
      style="{
        height: 100%;
        width: 100%;
        background-color: #f2f5f6;
        box-shadow: 0 0 6px rgba(0,0,0, .12);
        text-align: center;
        line-height: 40px;
        color: #1989fa;
      }"
    >
    TOP
    </div>
    </el-backtop>
    <!-- 头部导航 -->
    <div id="top-menu" class="dweb">

    </div>
    <!-- 侧边栏 -->
    <div id="left-menu" :class="'dweb '+mobile_left">
      <i @click="showHideLeftMenu" class="el-icon-menu" id="left-btn"></i>
      <!-- 导航栏 -->
      <el-row class="tac">
      <el-col :span="24" style="margin-top:80px">
        <div>
          <el-row>
            <el-col :span="12" ><el-avatar :size="50" :src="circleUrl"></el-avatar></el-col>
            <el-col :span="12" ><el-link type="primary">用户名</el-link></el-col>
          </el-row>
        </div>
        <el-menu
          class="el-menu-vertical-demo"
          background-color="#545c6400"
          text-color="#fff"
          active-text-color="#ffd04b"
          router
          @select="chooseMenu">
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-folder-opened"></i>
              <span>文章管理</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="/add-article">发布文章</el-menu-item>
              <el-menu-item index="/article-list">文章列表</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-menu-item index="/user-permission">
            <i class="el-icon-user"></i>
            <span slot="title">用户管理</span>
          </el-menu-item>
          <el-menu-item index="4">
            <i class="el-icon-money"></i>
            <span slot="title">打赏记录</span>
          </el-menu-item>
          <el-menu-item index="/lanmu-admin">
            <i class="el-icon-s-operation"></i>
            <span slot="title">栏目管理</span>
          </el-menu-item>
          <el-menu-item index="/user-socket">
            <i class="el-icon-chat-dot-round"></i>
            <span slot="title">在线聊天</span>
          </el-menu-item>
          <el-menu-item v-if="authUserLogin" @click="blogLogout()">
            <i class="el-icon-back"></i>
            <span slot="title">退出登录</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
    </div>
    <!-- 页面内容 -->
    <div id="content" :class="mobile_content">
      <router-view :screenWidth="screenWidth"></router-view>
      <!-- <div id="bg1" class="bgbox"></div>
      <div id="bg2" class="bgbox"></div>
      <div id="bg3" class="bgbox"></div> -->
      <!-- <el-image
      style="width: 100px; height: 100px"
      :src="url"
      :fit="'scale-down'"></el-image> -->
      <!-- 页脚 -->
      <div id="footer" class="dweb">
        <span>Copyright </span>
      </div>
    </div>

  </div>
</template>


<script>
  export default {
    data() {
      return {
        screenWidth:document.body.clientWidth,
        mobile_left:'',
        mobile_content:'',
        circleUrl: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"

      };
    },
    computed: {
      //验证用户是否登录
      authUserLogin(){
        //获取token
        return this.$store.getters.isnotUserlogin
      }
    },
    watch: {
      //监听用户token
      authUserLogin(newVal){
        if (newVal == null) {
          this.$router.push({path:'/login'})
        }

      }
    },
    created() {
      this.$store.dispatch('tryAutoLogin')
    },

    mounted() {
      
      // window.onresize = ()=>{
      //   this.screenWidth = document.body.clientWidth
      //   console.log(this.screenWidth)
      // }
      this.changeDevice()

    },
    methods: {
      chooseMenu(index){
        // console.log(index)
        this.$router.push({path:index})
      },
      changeDevice(){
        if(this.screenWidth <= 500) {
          this.mobile_left = 'xs'
          this.mobile_content = 'xs'
        }
      },
      showHideLeftMenu(){
        if(this.mobile_left == '') {
          this.mobile_left = 'xs'
        }else{
          this.mobile_left = ''
        }
        //宽屏
        if(this.screenWidth>500) {
          if(this.mobile_content == ''){
            this.mobile_content = 'xs'
          }else{
            this.mobile_content = ''
          }
        }
      },
      //退出登录
      blogLogout(){
        // this.$store.commit('clearUserinfo')
        // this.$router.push({path:'/'})
        this.$store.dispatch('blogLogout',this.$store.getters.isnotUserlogin)
      }
    }
  };
</script>

<style>
.el-col{
  margin-top: 5px;
}
</style>
