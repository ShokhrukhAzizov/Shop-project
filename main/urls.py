from django.urls import path
from .views import *

urlpatterns = [
    path('',index_page,name='home_page'),
    path('products/<slug:slug>/',products,name='products'),
    path('product/detail/<slug:slug>/',product_detail,name='product_detail'),
    path('comment/',comment_for_product,name='comment'),
    path('create/wish/<int:id>/', create_wish, name='create_wish_url'),
    path('favorites/', favorites, name='favorites'),
    path('delete_wish/', delete_wish, name='delete_wish'),
    path('contact/', contact_msg, name='contact'),
    path('my_cart/', my_cart, name='my_cart'),
    path('like/content/', like_content, name='like'),
]

