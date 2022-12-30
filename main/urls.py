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
    path('add/product/card', add_product_to_card, name='add_product_to_card_url'),
    path('decrease/product/card', decrease_product, name='decrease_product_url'),
    path('delete/product/card', delete_product_from_card, name='delete_product_from_card_url'),
    path('like/content/', like_content, name='like'),
]

