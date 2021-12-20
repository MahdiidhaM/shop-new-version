from django import template
from ..models import *
from cart.models import *

register = template.Library()

@register.inclusion_tag('shopping/tag.html',takes_context=True)
def Tag(context):
    request = context['request']
    usercurrent = request.user.is_authenticated
    if usercurrent:
        model = CategoryChild.objects.all() 
        usercart = request.user
        order,created = UserOrder.objects.get_or_create(author=usercart)
        modelcart = order.order_set.all()
    
        return {
            'model':model,
            'request':request,
            'modelcart':modelcart,
            'order':order,
        }
    else:
        model = CategoryChild.objects.all()
        return {
            'model':model,
        }

@register.inclusion_tag('shopping/tag2.html')
def Cat():
    model = CategoryChild.objects.all()
    return {
        'model':model
    }


# @register.simple_tag(name='simple',takes_context=True)
# def simple(context):
#     request = context['reqesut']
    
#     return {
#         'Blogs':model
#     }
