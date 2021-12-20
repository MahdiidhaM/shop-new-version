from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('',ProductView.as_view(),name='productView'),
    path('detail/<int:pk>',Detail,name='detail'),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',Logout,name='logout'),
    path('signup/',Signup,name='signup'),
    path('search/',Search,name='search'),
    path('update/',Update.as_view(),name='update'),
    path('viewlike/',viewlike,name='viewlike'),
    path('vote/<int:pk>/',vote,name='vote'),
    path('category/<int:pk>/',Category,name='category'),
    path('like/<int:pk>/',like,name='like'),
    path('dislike/<int:pk>/',dislike,name='dislike'),
    path('order/',record_order,name='order'),
]