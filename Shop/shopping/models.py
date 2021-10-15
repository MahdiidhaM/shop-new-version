from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DateField
from django.db.models.fields.related import ForeignKey 
# Create your models here.

class User(AbstractUser):
    author = models.BooleanField(default=False)
    address = models.CharField(max_length=500,blank=True,null=True)
    number = models.IntegerField(blank=True,null=True)
    zip_code = models.IntegerField(blank=True,null=True)
    plak = models.CharField(max_length=500,blank=True,null=True)
    Floor = models.IntegerField(blank=True,null=True)

class Category(models.Model):
    cat = models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.cat


class Inside(models.Model):
    inside = models.CharField(max_length=200,blank=True,null=True)
    relation = models.ManyToManyField(Category)
    def __str__(self):
        return self.inside


class Blog(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image_main = models.ImageField(upload_to='image')
    image_second = models.ImageField(upload_to='image',blank=True,null=True)
    image_third = models.ImageField(upload_to='image',blank=True,null=True)
    Price = models.IntegerField()
    quantity = models.IntegerField(blank=True,null=True)
    number = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    day = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __str__(self):
        return self.title
    @property
    def Imageurl(self):
        try:
            url = self.image_main.url
        except:
            url=''
        return url

    
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Blog,on_delete=models.CASCADE)
    date = DateField(auto_now_add=True)
    def __srt__(self):
        return str(self.author) + ' ' + str(self.comment)


class Like(models.Model):
    product_like = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user_like = models.ForeignKey(User,on_delete=models.CASCADE)
    def __srt__(self):
        return self.user_like + self.product_like


class Vote(models.Model):
    product = models.ForeignKey(Blog,on_delete=models.CASCADE,blank=True,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    vote = models.IntegerField(default=0,blank=True,null=True)


class Avrage(models.Model):
    product = models.ForeignKey(Blog,on_delete=models.CASCADE,blank=True,null=True)
    range_avrage = models.IntegerField(default=0,blank=True,null=True)

