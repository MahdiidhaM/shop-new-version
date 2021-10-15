from django.db.models import fields
from rest_framework import serializers
from shopping.models import Blog

class Blog_ser(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields='__all__'
    