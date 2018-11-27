from django.shortcuts import render
from django.template import RequestContext
from ordering_info.models import OrderDetail

# Create your views here.


def list_orderings(request):
    order_details = OrderDetail.objects.all()
    # shop_infos = ShopInfo.objects.all()
    # shop_orders = ShopOrder.objects.all()

    return render(request, 'ordering_info/orderinfo.html', {'order_posts': order_details}, RequestContext(request))


def show_detail(request, order_id):
    order_detail = OrderDetail.objects.get(id=order_id)
    if order_detail.salary <= 100:
        order_detail.salary = 6
    elif order_detail.salary > 100 and order_detail <= 200:
        order_detail.salary = 7
    else:
        order_detail.salary = 8
    order_detail.save()
    print(order_detail.__dict__)
    return render(request, 'ordering_info/order-detail.html', {'order_detail': order_detail}, RequestContext(request))
