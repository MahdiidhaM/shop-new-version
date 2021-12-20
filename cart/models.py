from django.db import models
from django.db.models.fields.related import ForeignKey
from shopping.models import Products,User 


class UserOrder(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.author)
    @property
    def sumitem(self):
        sumquantity = self.order_set.all()
        total = sum([i.quantity for i in sumquantity])
        return total
        
    @property
    def sumprice(self):
        sumquantity = self.order_set.all()
        total = sum([i.Sumprice for i in sumquantity])
        return total


class Order(models.Model):
    user = models.ForeignKey(UserOrder,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return str(self.user)+ ' ' + str(self.product)
    @property
    def Sumprice(self):
        total = self.quantity*self.product.Price
        return total

class OrderTotal(models.Model):
    products = models.ManyToManyField(Order)
    user = models.ForeignKey(UserOrder,on_delete=models.CASCADE)