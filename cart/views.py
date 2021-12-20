from django.shortcuts import render,redirect

from shopping.form import UpdateForm
from .models import Order,OrderTotal,UserOrder
from shopping.models import Products
from shopping.mixins import SuperRequiredMixin
from django.views.generic import ListView

# Show cart user 
def order(request):
    if request.user.is_authenticated:
        user = request.user
        order,created = UserOrder.objects.get_or_create(author=user)
        model = order.order_set.all()

        # Update product quantity 
        if request.method == 'POST':
            form = request.POST['num']
            pro = request.POST['sh']
            Order.objects.filter(product__id=pro,user=order).update(quantity=form)
        return render(request,'shopping/cart.html',{'blogs':model,'order':order})
    else:
        return redirect('login')

# Create cart user 
def Listcart(request,pk):
    blog = Products.objects.get(pk=pk)
    user = request.user
    if request.user.is_authenticated:
        order,created = UserOrder.objects.get_or_create(author=user)
        model,created = Order.objects.get_or_create(user=order,product=blog)
        return redirect('productView')
    else:
        return redirect('login')

def delete(request,pk):
    order = UserOrder.objects.get(author=request.user)
    Order.objects.filter(user=order,product=Products.objects.get(pk=pk)).delete()
    return redirect('Cart:carttoral')

class OrdersView(SuperRequiredMixin,ListView):
    queryset = OrderTotal.objects.all()
    template_name = 'shopping/my-account.html'


# Send all users cart to admin
def ordercard(request):
    if request.user.is_authenticated:
        model = UserOrder.objects.get(author=request.user)
        orders = model.order_set.all()
        return render(request,'shopping/checkout.html',{'orders':orders,'model':model})
    else:
        return redirect('login')
