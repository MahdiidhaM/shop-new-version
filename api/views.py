from functools import partial
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from shopping.models import Products, User, Vote
from shopping.models import Comment as products_commnets
from .serializer import *
from .permissions import Permission_View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class ListApi(ListAPIView):
    queryset = Products.objects.all()
    serializer_class = Blog_ser
    permission_classes = (Permission_View,)


class CreateCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class CartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = UserOrder.objects.get(author=request.user) # hit in database
        # cart = Order.objects.filter(user=user) # Order.objects.all() or get_or_create() or creat_or_update() and more...
        cart = user.order_set.all()
        serializer_cart = CartSerializer(cart, many=True)
        return Response(serializer_cart.data)

    def patch(self, request, pk):
        user = UserOrder.objects.get(author=request.user)
        cart = Order.objects.get(Q(pk=pk) & Q(user=user))
        print('------')
        print(cart)
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class LikeProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user)
        likes = user.like_set.all()
        serializer_like = LikeSerializer(likes, many=True)
        return Response(serializer_like.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class VoteProduct(APIView):

    # def quer(self, pk):
    #     print(pk)
    #     print('-------')
    #     product = Products.objects.get(pk=pk)
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        product = Products.objects.get(pk=pk)
        Vote.objects.get_or_create(author=request.user,product=product)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request, pk):
        product = Products.objects.get(pk=pk)
        serializer_product = ProductSerializer(product)
        serializer = VoteSerializer(data=request.data, context={'request':request, 'product':product})
        if serializer.is_valid():
            serializer.save()
            votes = Vote.objects.filter(product=product)
            rate = [ i.vote for i in votes ]
            avrrage = sum(rate)/len(rate)
            product.number = avrrage
            return Response(serializer_product.data)



class CommentList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        product = Products.objects.get(pk=pk)
        comment = products_commnets.objects.filter(comment=product, author=request.user)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        product = Products.objects.get(pk=pk)
        serializer_commnet = CommentSerializer(data = request.data, context={'request':request, 'product':product})
        if serializer_commnet.is_valid(raise_exception=True):
            serializer_commnet.save()
            return Response(serializer_commnet.data)
