from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from ordering_info.models import OrderDetail, OrderInfoForm

# Create your views here.


def list_orderings(request):
    order_details = OrderDetail.objects.all()
    # shop_infos = ShopInfo.objects.all()
    # shop_orders = ShopOrder.objects.all()

    return render(request, 'ordering_info/orderinfo.html', {'order_posts': order_details}, RequestContext(request))


def show_detail(request, order_id):
    order_detail = OrderDetail.objects.get(id=order_id)
    if order_detail.price <= 100:
        order_detail.salary = 6
    elif (order_detail.price > 100) and (order_detail.price <= 200):
        order_detail.salary = 7
    else:
        order_detail.salary = 8
    order_detail.save()
    return render(request, 'ordering_info/order-detail.html', {'order_detail': order_detail}, RequestContext(request))


def modify_order(request, order_id):
    order_detail = OrderDetail.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderInfoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            order_detail.dateTime = post.dateTime
            order_detail.keywords = post.keywords
            order_detail.enterChannel = post.enterChannel
            order_detail.scanDuration = post.scanDuration
            order_detail.talk = post.talk
            order_detail.shoppingCnt = post.shoppingCnt
            order_detail.orderCnt = post.orderCnt
            order_detail.price = post.price
            order_detail.charges = post.charges
            order_detail.memo = post.memo
            order_detail.salary = post.salary
            order_detail.finishStatus = post.finishStatus
            order_detail.moneyReturnStatus = post.moneyReturnStatus
            order_detail.exception = post.exception
            order_detail.remark = post.remark
            order_detail.userTaobaoId = post.userTaobaoId
            order_detail.save()

    return HttpResponseRedirect('/ordering_info/')


def delete_order(request, order_id):
    OrderDetail.objects.filter(id=order_id).delete()
    return HttpResponseRedirect('/ordering_info/')
