from alipay.aop.api.AlipayClientConfig import AlipayClientConfig    #客户端配置
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient  #默认客户端类
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo     #设置订单信息
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel  #网站支付数据模型类
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest  #网站支付请求类
from alipay.aop.api.util.SignatureUtils import verify_with_rsa      #加密签名

from website import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from blog.models import Article,PayOrder
import datetime
import random


@api_view(['POST'])
def getAlipayUrl(request):
    #查看登录
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')
    
    #获取用户，文章信息
    user = user_token[0].user
    article_id = request.POST['article_id']
    article = Article.objects.get(id=article_id)

    #生成订单
    nowtime = datetime.datetime.now()
    new_payorder = PayOrder(belong_user=user,belong=article)
    new_payorder.order = str(nowtime.year) + str(random.randrange(10000000,99999999))
    # print(new_payorder.order)
    new_payorder.price = '9.9'
    # new_payorder.save()


    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = settings.ALIPAY_URL
    alipay_client_config.app_id = settings.ALIPAY_APPID
    alipay_client_config.app_private_key = settings.APP_PRIVATE_KEY
    alipay_client_config.alipay_public_key = settings.ALIPAY_PUBLIC_KEY

    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
    model = AlipayTradePagePayModel()   #创建网站支付模型
    model.out_trade_no = new_payorder.order
    model.total_amount = new_payorder.price
    model.subject = "打赏订单："+new_payorder.order+'/'+new_payorder.price+'元'
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    model.timeout_express = "5m"

    #发送请求
    pay_request = AlipayTradePagePayRequest(biz_model=model)
    # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
    # pay_request.notify_url = settings.ALIPAY_NOTIFY_URL
    # pay_request.return_url = settings.ALIPAY_RETURN_URL
    response = client.page_execute(pay_request, http_method='GET')
    print(response)
    pay_link = response
    return Response({'pay_link':pay_link})