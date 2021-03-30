<template>
    <div id="add-article">
      <el-row :gutter="10">
          <el-col :xs="24" :lg="8">
              <div class="dweb">
                <el-form :label-position="labelPosition" label-width="80px" :model="article_info">
                    <el-form-item label="文章标题">
                        <el-input v-model="article_info.title"></el-input>
                    </el-form-item>
                    <el-form-item label="描述">
                        <el-input type="textarea" :rows="4" v-model="article_info.describe"></el-input>
                    </el-form-item>
                </el-form>
              </div>
          </el-col>
          <el-col :xs="24" :lg="16">
              <div class="dweb">
                  <div v-for="(img,index) in cover_list" :key="index"  >
                      <el-image
                        v-if="img == cover_img"
                        class="cover"
                        style="width: 150px; height: 150px"
                        :src="img"
                        :fit="'cover'"
                        @click="chooseCover(img)"></el-image>
                        <el-image
                        v-else
                        class=""
                        style="width: 150px; height: 150px"
                        :src="img"
                        :fit="'cover'"
                        @click="chooseCover(img)"></el-image>
                  </div>
                  <el-input
                    class="input-search"
                    placeholder="请输入内容"
                    prefix-icon="el-icon-search"
                    v-model="inputserach">
                  </el-input>
                  <el-button @click="searchImgurl" class="btn-search" type="primary" icon="el-icon-search">搜索</el-button>
                  <el-button @click="submitArticle" type="success" round>保存文章</el-button>
              </div>
          </el-col>
          <el-col :xs="24" :lg="24">
              <div class="dweb">
                  <div id="summernote"></div>
              </div>
          </el-col>
      </el-row>
    </div>
</template>

<script>
import $ from 'jquery'
import axios from 'axios'
import Qs from 'qs'
export default {
    data() {
        return {
            labelPosition: 'left',
            article_info:{
                title:"",
                describe:"",
                contents:""
            },
            cover_img:'',
            cover_list:[],
            inputserach: ''
        }
    },
    mounted() {
        this.summernote()
    },
    methods: {
        //查找爬取网址图片url
        searchImgurl(){
            let search_data ={
                 inputserach:this.inputserach
            }  
            axios.post('http://127.0.0.1:9000/api/search-img/',Qs.stringify(search_data))
            .then(res => {
                console.log(res);
            })
            .catch(err => {
                console.log(err);
            }) 
        },
        //提交文章
        submitArticle(){
            let article_data = {
                title: this.article_info.title,
                describe: this.article_info.describe,
                content: this.article_info.contents,
                cover: this.cover_img,
                token:this.$store.getters.isnotUserlogin
            }
            axios.post('http://127.0.0.1:9000/api/add-article/',Qs.stringify(article_data))
            .then(res => {
                console.log(res)
                if (res.data == 'nologin'){
                    alert('用户信息错误')
                    return
                }
                if (res.data == 'notitle'){
                    alert('文章标题不可为空')
                    return
                }
                if (res.data == 'nocover'){
                    alert('请选择文章封面')
                    return
                }
                if (res.data == 'ok'){
                    window.location.reload()
                    return
                }
                
                
            })
            .catch(err => {
                console.error(err);
            }) 
        },

        //调用富文本Summernote
        summernote(){
            let self = this
            $('#summernote').summernote({
                //提供编辑器默认参数
                width:"100%",
                height:500,
                lang: 'zh-CN',
                callbacks:{
                    // 当输入
                    onChange(contents){
                        self.article_info.contents = contents
                    },
                    //监听本地图片上传
                    onImageUpload(files){
                        
                        let img = files[0]
                        let imgData = new FileReader()
                        imgData.readAsDataURL(img)
                        
                        imgData.onload = function (){
                            
                            //插入图片
                            let imgnode = document.createElement('img')
                            imgnode.src = imgData.result
                            $('#summernote').summernote('insertNode',imgnode)
                            //推入封面待选择
                            self.cover_list.push(imgData.result)
                        }
                    },
                    //监听远程图片上传
                    onImageLinkInsert(url){
                        
                        //插入图片
                        let imgnode = document.createElement('img')
                        imgnode.src = url
                        
                        $('#summernote').summernote('insertNode',imgnode)
                        //推入封面待选择
                        self.cover_list.push(url)
                    },
                    //监听删除媒体文件
                    onMediaDelete(target){
                        console.log(target)
                        let imgData = target[0].src
                        console.log(imgData)
                        for (let i = 0; i < self.cover_list.length; i++){
                            if(self.cover_list[i] == imgData) {
                                self.cover_list.splice(i,1)
                            }
                        }
                    }
                }
            });
        },
        //选择封面
        chooseCover(img){
            this.cover_img = img
        }
    },
};
</script>

<!-- 使用scoped可防止污染其它组件中的样式 -->
<style scoped>
.dweb {
    min-height: 200px;
    padding: 20px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
 }

.dweb .el-button {
    position: fixed;
    right: 20px;
    z-index: 1001;
    margin-top: 260px;
}

.dweb .input-search {
    position: absolute;
    max-width: 200px;
    right: 200px;
    z-index: 1001;
    margin-top: 260px;
}
.dweb .btn-search {
    position: absolute;
    right: 140px;
    z-index: 1001;
    margin-top: 260px;
}

.dweb .el-image:hover {
    border: 2px solid rgb(255, 208, 0);
}
.dweb .el-image.cover {
    border: 2px solid rgb(255, 208, 0);
}

.el-form-item {
    margin-top: 22px;
}
/* 此处样式为局部样式被颜色无法影响框架样式，所以改至mystyle.css中修改 */
/* .el-form-item__label {
    color: #fff!important;
} */
</style>