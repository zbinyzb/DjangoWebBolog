# api路由填写
from django.urls import path
from blog import api,payapi

urlpatterns = [
    #文章管理
      #文章数据 查看
      path('article-data/', api.articleData),
      #文章发布
      path('add-article/', api.add_article),
      #文章列表
      path('article-list/', api.articleList),
      #文章删除
      path('delete-article/', api.delete_article),
    #用户管理
      #登录
      path('zbin-login/',api.zbin_login), 
      #注册
      path('zbin-register/',api.zbin_register),
      #自动登录
      path('auto-login/',api.zbin_autologin),
      #登出
      path('zbin-logout/',api.zbin_logout),
      #鉴权
      path('zbin-checkperm/',api.zbin_checkperm),
      #用户列表
      path('zbin-userlist/',api.zbin_userlist),
    #用户组
      path('zbin-group/',api.zbin_group),
    #栏目管理
      path('zbin-lanmu/',api.zbin_lanmu),
    #文章用户互动
      #评论
      path('pinglun/',api.zbinPinglun),
      #点赞收藏打赏
      path('user-article-info/',api.userArticleInfo),
      path('article-like/',api.articleLike),
      path('article-favor/',api.articleFavor),
      path('get-alipay-url/',payapi.getAlipayUrl),
      
      

]