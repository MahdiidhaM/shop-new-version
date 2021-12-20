from django.contrib import admin
from .models import  UserOrder, Order ,OrderTotal
# Register your models here.
 

admin.site.register(UserOrder)
admin.site.register(Order)
admin.site.register(OrderTotal)