from django.shortcuts import render
from rest_framework.generics import ListAPIView
from shopping.models import Products
from .serializer import Blog_ser
from .permissions import Permission_View
class ListApi(ListAPIView):
    queryset = Products.objects.all()
    serializer_class = Blog_ser
    permission_classes = (Permission_View,)

