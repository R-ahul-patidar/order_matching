

from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_and_match_page, name='order_and_match_page'),
    # path('order_summary/', views.order_summary, name='order_summary'),
]
