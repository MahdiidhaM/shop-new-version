from django import forms
from .models import Comment, User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']


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

