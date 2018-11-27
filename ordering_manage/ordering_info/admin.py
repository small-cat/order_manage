from django.contrib import admin

from ordering_info.models import ShopInfo, ShopOrder, OrderDetail

# Register your models here.


class ShopInfoAdmin(admin.ModelAdmin):
    list_display = ('shopName', 'shopId', 'get_shop_type')


class ShopOrderAdmin(admin.ModelAdmin):
    list_display = ('dateTime', 'get_shop_name', 'itemName', 'requirements')


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('dateTime', 'get_shop_name', 'get_item_name', 'orderCnt', 'price', 'userTaobaoId')


admin.site.register(ShopInfo, ShopInfoAdmin)
admin.site.register(ShopOrder, ShopOrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
