from django import forms
from django.db.models import fields
from django.forms.models import ModelForm

from cart.models import Order
from .models import Comment, User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','number','email','password1','password2']

class SmsForm(forms.Form):
    sms = forms.CharField(max_length=6)

class CommentForm(forms.Form):
    class Meta:
        model = Comment
        fields = ['text']

class UpdateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):

        user = kwargs.pop('user')
        super(UpdateForm,self).__init__(*args,**kwargs)
    class Meta:
        model = User
        fields = ['username','address','number','zip_code','plak','Floor']
    
class Reset_Form(forms.Form):
    phone = forms.IntegerField()
        
class Quit_Form(forms.ModelForm):
    class Meta:    
        model = Order
        fields = ['quantity']
