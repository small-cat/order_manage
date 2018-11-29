from django.contrib import admin

from ordering_info.models import ShopInfo, ShopOrder, OrderDetail, UserInfo

# Register your models here.


class ShopInfoAdmin(admin.ModelAdmin):
    list_display = ('shopName', 'shopId', 'get_shop_type')


class ShopOrderAdmin(admin.ModelAdmin):
    list_display = ('dateTime', 'get_shop_name', 'itemName', 'requirements')


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('dateTime', 'get_shop_name', 'get_item_name', 'orderCnt', 'price', 'userTaobaoId')


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('userTaobaoId', 'wxName', 'recommendWxName', 'wxGroupName')


admin.site.register(ShopInfo, ShopInfoAdmin)
admin.site.register(ShopOrder, ShopOrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
