from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment,Like,User,Vote,Avrage
from django.views.generic import ListView,UpdateView
from .form import SignupForm,CommentForm, UpdateForm
from cart.models import main,aun,Order
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .mixins import SuperRequiredMixin
from django.utils import timezone
from django.db.models import Q

# Create your views here.

class ProductView(ListView):
    queryset = Blog.objects.all()
    template_name = 'shopping/index.html' 
    def get_context_data(self, **kwargs):
        time = timezone.now().day-2
        context = super().get_context_data(**kwargs)
        context['time'] = Blog.objects.filter(day__day__gte=time)[:6]
        context['avrage'] = Avrage.objects.filter(range_avrage__gte=8)
        # for i in Like.objects.filter(user_like=self.request.user):
        #     x=i.product_like
        # context['like'] = x
        return context


def Detail(request,pk):
    blogs = Blog.objects.get(pk=pk)
    comments = blogs.comment_set.all()
    model = Vote.objects.filter(product=blogs.id)
    similars = Blog.objects.filter(category=blogs.category)
    x = [i.vote for i in model ]
    if len(x)>0:
        avrage = sum(x)/len(x)
    else:
        avrage=0
    if request.user.is_authenticated:
        create = Vote.objects.get_or_create(author=request.user,product=blogs)
        
        view_avrage,created = Avrage.objects.get_or_create(product=blogs)
        view_avrage = Avrage.objects.filter(product=blogs).update(range_avrage=avrage)
        
        if request.method == "POST":
            form = request.POST['comment']
            model = Comment.objects.create(author=request.user,comment=blogs,text=form)
    context={
        'blog':blogs,'comment':comments,
        'avrage':avrage,'similars':similars
    }
    return render(request,'shopping/shop-detail.html',context)
    

def Login(request):
    form = request.POST
    if request.method == 'POST':
        model = authenticate(request,password=form['password'],username=form['username'])
        if model is not None:
            login(request,model)
            return redirect('productView')
        return render(request,'shopping/login.html',{'form':form})
    return render(request,'shopping/login.html',{'form':form})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def Search(request):
    if request.method == 'POST':
        searchs = request.POST['search']
        model = Blog.objects.filter(title__contains=request.POST['search'])
    context = {'search':model,'searchs':searchs}
    return render(request,'shopping/search.html',context)

def Signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'shopping/signup.html',{'form':form})

def Listcart(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    order,created = main.objects.get_or_create(author=user)
    model,created = aun.objects.get_or_create(user=order,product=blog)
    if request.user.is_authenticated:
        return redirect('productView')
    else:
        return redirect('login')

def order(request):
    if request.user.is_authenticated:
        user = request.user
        order,created = main.objects.get_or_create(author=user)
        model = order.aun_set.all()
        if request.method == 'POST':
            form = request.POST['num']
            pro = request.POST['sh']
            update = aun.objects.filter(product__id=pro,user=order).update(quantity=form)
        return render(request,'shopping/cart.html',{'blogs':model,'order':order})
    else:
        return redirect('login')

def Category(request,pk):
    cat = Blog.objects.filter(category__id=pk)
    return render(request,'shopping/shop.html',{'cats':cat})

def like(request,pk):
    if request.user.is_authenticated:
        blog = Blog.objects.get(pk=pk)
        favorite,created = Like.objects.get_or_create(user_like=request.user,product_like=blog)
        order,created = User.objects.get_or_create(username=request.user)
        userloe = order.like_set.all()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('login')

@login_required
def viewlike(request):
    order,created = User.objects.get_or_create(username=request.user)
    userloe = order.like_set.all()
    return render(request,'shopping/like.html',{'favorite':userloe})


def delete(request,pk):
    order = main.objects.get(author=request.user)
    model = aun.objects.filter(user=order,product=Blog.objects.get(pk=pk)).delete()
    return redirect('main')


def vote(request,pk):
    model = Blog.objects.get(pk=pk)
    if request.method == "POST":
        form = request.POST['vote']
        vote = Vote.objects.filter(product=model,author=request.user).update(vote=form)
    return redirect('detail',pk=model.pk)

def dislike(request,pk):
    dislike = Like.objects.filter(product_like=Blog.objects.get(pk=pk),user_like=request.user).delete()
    return redirect('viewlike')

from django.urls.base import reverse_lazy
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
    user,created = main.objects.get_or_create(author=request.user)
    # pro = user.aun_set.all()
    look = aun.objects.filter(user=user)
    order,created = Order.objects.get_or_create(user=user)
    for i in look:
        order.products.add(i.id)
    
    return render(request,'shopping/end_ordering.html',{'order':order,'user_info':user})

class OrdersView(SuperRequiredMixin,ListView):
    queryset = Order.objects.all()
    template_name = 'shopping/my-account.html'

# def done(request,pk):
#     model = Order.objects.get(pk=pk)

def ordercard(request):
    if request.user.is_authenticated:
        model = main.objects.get(author=request.user)
        orders = model.aun_set.all()
        return render(request,'shopping/checkout.html',{'orders':orders,'model':model})
    else:
        return redirect('login')


