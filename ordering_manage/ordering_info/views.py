from django.core.paginator import Paginator
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from ordering_info.models import OrderDetail, OrderInfoForm

# Create your views here.


def list_orderings(request):
    order_details_lists = OrderDetail.objects.all()
    paginator = Paginator(order_details_lists, 20)
    page = request.GET.get('page')
    order_details = paginator.get_page(page)

    return render(request, 'ordering_info/index.html', {'order_posts': order_details}, RequestContext(request))


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


def search_orders(request):
    datetime = request.GET.get('datetime')
    keywords = request.GET.get('keywords')
    finish_status = request.GET.get('finishStatus')
    money_return_status = request.GET.get('moneyReturnStatus')
    user_taobao_id = request.GET.get('userTaobaoId')

    print(datetime, keywords, finish_status, money_return_status, user_taobao_id)

    # filter
    results = OrderDetail.objects.filter(finishStatus=finish_status).filter(moneyReturnStatus=money_return_status)
    if datetime:
        results = results.filter(dateTime=datetime)
    if keywords:
        results = results.filter(keywords__contains=keywords)
    if user_taobao_id:
        results = results.filter(userTaobaoId__contains=user_taobao_id)

    paginator = Paginator(results, 20)
    page = request.GET.get('page')
    order_posts = paginator.get_page(page)

    return render(request, 'ordering_info/index.html', {'order_posts': order_posts}, RequestContext(request))


def show_userinfo(request, user_id):
    print('userinfo')
