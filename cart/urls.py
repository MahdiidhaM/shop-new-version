from django.urls import path
from .views import OrdersView,order,Listcart,delete,ordercard


app_name='Cart'
urlpatterns = [
    path('carttoral/',order,name='carttoral'),
    path('cart/<int:pk>/',Listcart,name='cart'),
    path('delete/<int:pk>/',delete,name='delete'),
    path('ordersview/',OrdersView.as_view(),name='ordersview'),
    path('ordercard/',ordercard,name='ordercard'),
]