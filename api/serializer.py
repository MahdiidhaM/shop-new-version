from pyexpat import model
from django.db.models import fields
from rest_framework import serializers
from shopping.models import Like, Products, Vote, Comment
from cart.models import *


class Blog_ser(serializers.ModelSerializer):

    class Meta:
        model=Products
        fields='__all__'
    

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        final_user,created = UserOrder.objects.get_or_create(author=user)
        validated_data['user'] = final_user 
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance


class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_like'] = user 
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Products
        fields = '__all__'



class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        product = self.context['product']
        return Vote.objects.filter(author=user,product=product).update(vote=validated_data['vote'])


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.CharField(source='user.username')
    class Meta:
        model = Comment
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = self.context['product']
        validated_data['author'] = user
        validated_data['comment'] = product
        return super().create(validated_data)
