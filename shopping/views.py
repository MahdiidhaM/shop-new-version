from .form import SignupForm,CommentForm, UpdateForm,Reset_Form,SmsForm,Quit_Form
from .models import Products, Comment,Like,User,Vote,Avrage
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,UpdateView
from cart.models import UserOrder,Order,OrderTotal
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from .mixins import SuperRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from random import randint
from django.conf import *
import kavenegar


class ProductView(ListView):
    queryset = Products.objects.all()
    template_name = 'shopping/index.html' 
    def get_context_data(self, **kwargs):
        time = timezone.now().day-2                  
        context = super().get_context_data(**kwargs)
        context['time'] = Products.objects.filter(day__day__gte=time)[:6]   # Query for newest products
        context['avrage'] = Avrage.objects.filter(range_avrage__gte=8)      # Query for the most vote by users to the products
        return context


def Detail(request,pk):
    product = Products.objects.get(pk=pk)
    comments = product.comment_set.all()                            # Comments for each Product
    model = Vote.objects.filter(product=product.id)                 # Get total votes for each Product  
    similars = Products.objects.filter(category=product.category)
    
    # Calculate The avrage for each product
    rate = [i.vote for i in model ]
    if len(rate)>0:
        avrage = sum(rate)/len(rate)
    else:
        avrage=0
    if request.user.is_authenticated:
        Vote.objects.get_or_create(author=request.user,product=product)
        view_avrage,created = Avrage.objects.get_or_create(product=product)
        Avrage.objects.filter(product=product).update(range_avrage=avrage)
        # Get comment user and set user and product for it
        if request.method == "POST":
            form = request.POST['comment']
            model = Comment.objects.create(author=request.user,comment=product,text=form)

    context={
        'blog':product,'comment':comments,
        'avrage':avrage,'similars':similars,
            }
    return render(request,'shopping/shop-detail.html',context)

def Logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # redirect user to current page

def Search(request):
    if request.method == "POST":
        searchs = request.POST['search']
        model = Products.objects.filter(title__contains=request.POST['search'])
        context = {'search':model,'searchs':searchs}
        return render(request,'shopping/search.html',context)
    else:
        return render(request,'shopping/search.html')


# Set up the user registration by sms without saveing data in database
# All process registration do it in single page
token = 0
user_form_data = ''
def Signup(request):
    form = SignupForm()
    sms = SmsForm()

    if 'username' and 'password1' and 'password2' and 'number' and 'email' in request.POST : 
        form = SignupForm(request.POST)
        print(form.errors)
        print(len(request.POST['number']))
        if form.is_valid():
            global token,user_form_data   # Set confirm code and data form user
            user_form_data = form 
            token = randint(1000, 9999) 
            print('====================> token',token)
            phone_number = request.POST['number']
            try:
                api = kavenegar.KavenegarAPI(settings.KAVENEGAR_APIKEY)
                message1 = f'کد تاییدیه\n {token}'
                params = {
                    'sender': '1000596446',
                    'receptor': phone_number,
                    'message': message1,
                        }
                response = api.sms_send(params)
            except kavenegar.APIException as e:
                print(e)
            except kavenegar.HTTPException as e:
                print(e)
            return render(request,'shopping/signup.html',{'SmsForm':sms}) # if user form is valid render sms form
    # save user information if token value equal to code confirm
    elif 'sms' in request.POST:    
        if int(request.POST['sms']) == token:
            user_form_data.save()
            return redirect('/')
            
    else:
        form = SignupForm()
    return render(request,'shopping/signup.html',{'form':form})

def Category(request,pk):
    cat = Products.objects.filter(category__id=pk)
    return render(request,'shopping/shop.html',{'cats':cat})

def like(request,pk):
    if request.user.is_authenticated:
        blog = Products.objects.get(pk=pk)
        favorite,created = Like.objects.get_or_create(user_like=request.user,product_like=blog)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('login')

@login_required
def viewlike(request):
    order,created = User.objects.get_or_create(username=request.user)
    userloe = order.like_set.all()
    return render(request,'shopping/like.html',{'favorite':userloe})

def vote(request,pk):
    model = Products.objects.get(pk=pk)
    if request.method == "POST":
        form = request.POST['vote']
        Vote.objects.filter(product=model,author=request.user).update(vote=form) # Each user can just one vote register
    return redirect('detail',pk=model.pk)

def dislike(request,pk):
    Like.objects.filter(product_like=Products.objects.get(pk=pk),user_like=request.user).delete()
    return redirect('viewlike')


# chagne user information such as address number and ... 
class Update(UpdateView):
    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('main')
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)
    def get_form_kwargs(self):
        kw = super(Update,self).get_form_kwargs()
        kw.update({
            'user':self.request.user
        })
        return kw

def record_order(request):
    user,created = UserOrder.objects.get_or_create(author=request.user)
    look = Order.objects.filter(user=user)
    order,created = OrderTotal.objects.get_or_create(user=user)
    Order.objects.filter(user=user).delete()
    messages.success(request,'خرید شما با موفقیت افزوده شد')
    return redirect('/')