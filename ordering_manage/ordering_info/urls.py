# ordering_info urls

from django.urls import path
from ordering_info.views import *

app_name = 'ordering_info'
urlpatterns = [
    path('', list_orderings, name='list orderings'),
    path('<int:order_id>/show_details/', show_detail, name='show detail'),
    path('<int:order_id>/modify-info/', modify_order, name='modify info'),
    path('<int:order_id>/delete/', delete_order, name="delete order"),
]
