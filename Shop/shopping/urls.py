from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('',ProductView.as_view(),name='productView'),
    path('detail/<int:pk>',Detail,name='detail'),
    # path('login/',Login,name='login'), 
    path('login/',LoginView.as_view(), name='login'),
    path('main/',order,name='main'),
    path('logout/',Logout,name='logout'),
    path('signup/',Signup,name='signup'),
    path('search/',Search,name='search'),
    path('update/',Update.as_view(),name='update'),
    path('viewlike/',viewlike,name='viewlike'),
    path('vote/<int:pk>/',vote,name='vote'),
    path('cart/<int:pk>/',Listcart,name='cart'),
    path('category/<int:pk>/',Category,name='category'),
    path('like/<int:pk>/',like,name='like'),
    path('delete/<int:pk>/',delete,name='delete'),
    path('dislike/<int:pk>/',dislike,name='dislike'),
    path('order/',record_order,name='order'),
    path('ordersview/',OrdersView.as_view(),name='ordersview'),
    path('ordercard/',ordercard,name='ordercard'),
]