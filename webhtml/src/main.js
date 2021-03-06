import Vue from 'vue'
import ElementUI from 'element-ui'
import App from './App.vue'
import store from './store'
import router from './router'
//引用ElementUI样式
import 'element-ui/lib/theme-chalk/index.css';
import './assets/css/mystyle.css'

//引入iconfont
import './assets/css/icon/iconfont.css'

//引入summernote
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import 'popper.js'
import 'summernote' 
import 'summernote/lang/summernote-zh-CN.js'
import 'summernote/dist/summernote.css'


//引用ElementUI
Vue.use(ElementUI)
Vue.config.productionTip = false
Vue.config.devtools = true;
new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
