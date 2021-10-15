from django import template
from ..models import *
from cart.models import *

register = template.Library()

@register.inclusion_tag('shopping/tag.html',takes_context=True)
def Tag(context):
    request = context['request']
    usercurrent = request.user.is_authenticated
    if usercurrent:
        model = Inside.objects.all() 
        usercart = request.user
        order,created = main.objects.get_or_create(author=usercart)
        modelcart = order.aun_set.all()
    
        return {
            'model':model,
            'request':request,
            'modelcart':modelcart,
            'order':order,
        }
    else:
        model = Inside.objects.all()
        return {
            'model':model,
        }

@register.inclusion_tag('shopping/tag2.html')
def Cat():
    model = Inside.objects.all()
    return {
        'model':model
    }


# @register.simple_tag(name='simple',takes_context=True)
# def simple(context):
#     request = context['reqesut']
    
#     return {
#         'Blogs':model
#     }
