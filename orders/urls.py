from django.urls import path
from soundlab_store.views import OrderListCreateView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-create'),
]




