from django.db.models import fields
from rest_framework import serializers
from shopping.models import Products

class Blog_ser(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields='__all__'
    