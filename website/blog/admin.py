from django.contrib import admin
from blog.models import Article,Userinfo,Lanmu,Pinlun,Favourite,Like,PayOrder
# Register your models here.
admin.site.register(Article)
admin.site.register(Userinfo)
admin.site.register(Lanmu)
admin.site.register(Pinlun)
admin.site.register(Favourite)
admin.site.register(Like)
admin.site.register(PayOrder)
