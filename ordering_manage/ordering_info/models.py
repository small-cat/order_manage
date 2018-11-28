from django.db import models
from django import forms

# Create your models here.


class ShopInfo(models.Model):
    # shop info

    SHOP_TYPE_CHOICES = (
        (0, 'known'),
        (1, 'taobao'),
        (2, 'tmall')
    )
    shopId = models.CharField(max_length=40)
    shopName = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=16)   # 0 - null
    shopType = models.SmallIntegerField(choices=SHOP_TYPE_CHOICES)           # 0 - null; 1 - taobao; 2 - Tmall

    def get_shop_type(self):
        shop_types = ['known', 'taobao', 'tmall']
        return shop_types[self.shopType]
    get_shop_type.short_description = 'ShopType'


class ShopOrder(models.Model):
    # shop order
    dateTime = models.DateField()
    shopId = models.ForeignKey(ShopInfo, on_delete=models.CASCADE)
    itemLink = models.URLField()
    itemName = models.CharField(max_length=64)
    itemCode = models.CharField(max_length=12)
    remark = models.TextField()
    requirements = models.TextField()

    def get_shop_name(self):
        return self.shopId.shopName
    get_shop_name.short_description = 'ShopName'


class OrderDetail(models.Model):
    # order details
    # 已完成、未完成、未返款、已返款
    FINISH_STATUS_CHOICES = (
        (-1, '异常'),
        (0, '未完成'),
        (1, '已完成')
    )

    RETURN_MONEY_CHOICES = (
        (-1, '异常'),
        (0, '未返款'),
        (1, '已返款')
    )

    TALK_CHOICES = (
        (0, '否'),
        (1, '是')
    )

    EXCEPTION_CHOICES = (
        (0, '错误'),
        (1, '正确')
    )
    dateTime = models.DateField()
    itemCode = models.ForeignKey(ShopOrder, on_delete=models.CASCADE)
    keywords = models.CharField(max_length=64)      # max length of keywords is 60 bytes
    enterChannel = models.CharField(max_length=24)
    scanDuration = models.SmallIntegerField()       # time of scan shopping items
    # whether need to talk with custome service staff or not
    talk = models.SmallIntegerField(choices=TALK_CHOICES)
    shoppingCnt = models.SmallIntegerField()        # number of purchased items
    # item should be purchased orderCnt times that could be searched by the keywords
    orderCnt = models.SmallIntegerField()
    price = models.FloatField()                     # price of item
    charges = models.FloatField()                   # our salary
    memo = models.TextField()                       # customers' memos
    salary = models.FloatField()                    # employees' salary each order
    # status of order: -1 - exception, 0 - unfinished, 1 - finished.
    # the order is  finished only after payed by customers
    finishStatus = models.SmallIntegerField(choices=FINISH_STATUS_CHOICES)
    # 0 - not return, 1 - had returned, -1 - exception
    moneyReturnStatus = models.SmallIntegerField(choices=RETURN_MONEY_CHOICES)
    # description of exceptions. If one order occured an exception, finishedStatus and moneyReturnStatus should be -1
    exception = models.SmallIntegerField(choices=EXCEPTION_CHOICES)
    remark = models.TextField()
    userTaobaoId = models.CharField(max_length=64, null=True)

    def get_shop_name(self):
        return self.itemCode.shopId.shopName
    get_shop_name.short_description = 'ShopName'

    def get_item_name(self):
        return self.itemCode.itemName
    get_item_name.short_description = 'ItemName'


class OrderInfoForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        # itemCode is foreign key, in form it can not modify directly, so fields doesn't contain itemCode.
        # but itemCode should be processed when modify order info
        fields = ('dateTime', 'keywords', 'enterChannel', 'scanDuration', 'talk', 'shoppingCnt',
                  'orderCnt', 'price', 'charges', 'memo', 'salary', 'finishStatus', 'moneyReturnStatus',
                  'exception', 'remark', 'userTaobaoId')
