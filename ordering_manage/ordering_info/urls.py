# ordering_info urls

from django.urls import path
from ordering_info.views import *

urlpatterns = [
    path('', list_orderings, name='list orderings'),
    path('<int:order_id>/show_details/', show_detail, name='show detail'),
]
