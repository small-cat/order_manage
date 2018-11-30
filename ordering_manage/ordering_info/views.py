from django.core.paginator import Paginator
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from ordering_info.models import OrderDetail, OrderInfoForm, UserInfo

# Create your views here.


def list_orderings(request):
    order_details_lists = OrderDetail.objects.all().order_by('dateTime')
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
            print('finishStatus:' + post.finishStatus)
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

    # filter
    results = OrderDetail.objects.filter(finishStatus=finish_status)\
        .filter(moneyReturnStatus=money_return_status).order_by('dateTime')
    if datetime:
        results = results.filter(dateTime=datetime)
    if keywords:
        results = results.filter(keywords__contains=keywords)
    if user_taobao_id:
        results = results.filter(userTaobaoId__userTaobaoId__contains=user_taobao_id)

    paginator = Paginator(results, 20)
    page = request.GET.get('page')
    order_posts = paginator.get_page(page)

    return render(request, 'ordering_info/index.html', {'order_posts': order_posts}, RequestContext(request))


def show_userinfo(request, user_id):
    err_msg = ''
    user_info = UserInfo.objects.filter(id__exact=user_id)
    if not user_info.exists():
        err_msg = '当前搜索用户不存在，请确保搜索输入正确或添加新用户信息'

    return render(request, 'ordering_info/user-info.html', {'user_info': user_info, 'err_msg': err_msg},
                  RequestContext(request))


def search_userinfo(request):
    user_taobao_name = request.GET.get('userTaobaoId')
    user_wxname = request.GET.get('wxName')
    user_recommend_wxname = request.GET.get('recommendWxName')
    user_wx_group_name = request.GET.get('wxGroupName')
    err_msg = ''
    user_info = UserInfo.objects.all()

    if user_taobao_name or user_wxname or user_recommend_wxname or user_wx_group_name:
        if user_taobao_name:
            user_info = user_info.filter(userTaobaoId__contains=user_taobao_name)
        if user_wxname:
            user_info = user_info.filter(wxName__contains=user_wxname)
        if user_recommend_wxname:
            user_info = user_info.filter(recommendWxName__contains=user_recommend_wxname)
        if user_wx_group_name:
            user_info = user_info.filter(wxGroupName__contains=user_wx_group_name)

    if not user_info.exists():
        err_msg = '当前搜索用户不存在，请确保搜索输入正确或添加新用户信息'

    paginator = Paginator(user_info, 20)
    page = request.GET.get('page')
    user_infos = paginator.get_page(page)
    return render(request, 'ordering_info/user-info.html', {'user_info': user_infos, 'err_msg': err_msg},
                  RequestContext(request))


def add_user(request):
    if request.method == 'POST':
        new_user = UserInfo(
            userTaobaoId=request.POST.get('newUserTaobaoId'),
            wxName=request.POST.get('newWxName'),
            recommendWxName=request.POST.get('newRecommendWxName'),
            wxGroupName=request.POST.get('newWxGroupName'),
            remark=request.POST.get('newRemark')
        )

        if new_user.userTaobaoId:
            new_user.save()

    return HttpResponseRedirect('/ordering_info/search_userinfo/')
