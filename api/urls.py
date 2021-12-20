from django.urls import path
from .views import *


urlpatterns = [
    path('',ListApi.as_view(),name='list')
]
