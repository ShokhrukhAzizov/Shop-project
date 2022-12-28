from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def PagenatorPage(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


def index_page(request):
    category = Category.objects.all()
    my_dict = {}
    for cat in Category.objects.all():
        pros = Product.objects.filter(category=cat).count()
        my_dict[cat]=pros

    query = request.GET.get('search')
    if query is not None and query != '':
        category = Category.objects.filter(Q(name__icontains=query))
    context = {
        'category':category,
        'my_dict':my_dict
    }
    return render(request,'index.html',context)

def products(request,slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    product = Product.objects.all()
    my_comment = {}
    for pro in product:
        comment = Comment.objects.filter(product=pro).count()
        my_comment[pro]=comment
        
    query = request.GET.get('search')
    if query is not None and query != '':
        products = Product.objects.filter(Q(title__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query))
    context = {
        'my_comment':my_comment,
        'category':category,
        'products':PagenatorPage(products,6,request)

    }
    return render(request,'listing-page.html',context)

def product_detail(request,slug):
    user = request.user
    product = Product.objects.get(slug=slug)
    comment = Comment.objects.filter(product=product)
    like = Likee.objects.filter(product=product).count()
    product_excluded = Product.objects.filter(category=product.category).exclude(id=product.id)[:3]
    query = request.GET.get('search')
    if query is not None and query != '':
        comment = Comment.objects.filter(Q(text__icontains=query, product__id=product.id))
    context = {
        'product':product,
        'comment':comment,
        'product_filtered':product_excluded,
        'user':user,
        'like':like
        
    }
    return render(request,'detail-page.html',context)

def comment_for_product(request):
    text = request.POST['text']
    id = request.POST['id']
    product = Product.objects.get(id=id)
    Comment.objects.create(
        text=text,
        product=product,
        user=request.user
    )
    return redirect('product_detail',product.slug)

def create_wish(request, id):
    product = Product.objects.get(id=id)
    wishlist = Wishlist.objects.filter(user=request.user, product=product).count()
    if wishlist == 1:
        if request.method == 'POST':
            id = request.POST['id']
            wish = Wishlist.objects.get(id=id)
            wish.delete()

    elif wishlist == 0:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )

    # try:
    #     object = Wishlist.objects.get(user=request.user,product=product)
    #     print(object)
    # except MultipleObjectsReturned:
    #     print(3)
    #     # Wishlist.objects.create(
    #     #     user=request.user,
    #     #     product=product
    #     # )
    # except ObjectDoesNotExist:
    #     print(2)
    # try:
    #     wishlist = Wishlist.objects.get(user=request.user,product=product)
    #     wishlist.product == 1
    #     wishlist.save() 
    # except:
    #     Wishlist.objects.create(
    #     user=request.user,
    #     product=product
    #     )
    return redirect('product_detail',product.slug)

def favorites(request):
    user = request.user
    product = Product.objects.all()
    wish = Wishlist.objects.filter(user=user)
    context = {
        'wish':wish,
        'user':user,
        'product':product
    }
    return render(request,'favorite.html',context)


def delete_wish(request):
    id = request.POST['id']
    wish_deleting = Wishlist.objects.get(id=id)
    wish_deleting.delete()
    return redirect('favorites')

def contact_msg(request):
    if request.method == 'POST':
        subject = request.POST['name']
        message = request.POST['message']
        email = request.POST['email']
        send_mail(
            subject=subject,
            from_email=email,
            message=message,
            recipient_list=['sardorbek1547@gmail.com']
        )

    return render(request,'contact.html')
    


def my_cart(request):
    return render(request,'my_cart.html') 

def like_content(request):
    pro_id = request.POST['id']
    product = Product.objects.get(id=pro_id)
    try:
        Likee.objects.get(user=request.user,product=product)
        Likee.save()
    except:
        Likee.objects.create(
            product=product,
            user=request.user
        )

        return redirect('product_detail',product.slug)