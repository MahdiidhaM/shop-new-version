from django.urls import path
from .views import *


urlpatterns = [
    path('', ListApi.as_view(),name='list'),
    path('createcart/', CreateCart.as_view(),name='createcart'),
    path('cartdetail/<int:pk>', CartDetail.as_view(), name='cartdetail'),
    path('cartdetail/', CartDetail.as_view(), name='cartdetail'),
    path('likeproduct/', LikeProduct.as_view(), name='likeproduct'),
    path('voteproduct/<int:pk>', VoteProduct.as_view(), name='voteproduct'),
    path('comment/<int:pk>', CommentList.as_view(), name='comment')
]
