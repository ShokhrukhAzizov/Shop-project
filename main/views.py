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
    card = Card.objects.filter(user=request.user, is_active=True).last()
    products = ProductCard.objects.filter(card=card)
    quantity = 0
    total_sum = 0
    for product in products:
        price = product.product.price * product.quantity
        total_sum +=price
        quantity += product.quantity
    context = {
        'card':card,
        'products':products,
        'total_sum':total_sum,
        'quantity':quantity
    }
    return render(request,'my_cart.html', context) 

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


def add_product_to_card(request):
    product_id = request.POST['product_id']
    product = Product.objects.get(id=product_id)
    card = Card.objects.filter(user=request.user).last()
    if card is None:
        card = Card.objects.create(user=request.user)
    product_card_quantity = ProductCard.objects.filter(product=product, card=card).count()
    if product_card_quantity == 0:
        product_card = ProductCard.objects.create(card=card, product=product)
    elif product_card_quantity == 1:
        product_card = ProductCard.objects.get(card=card, product=product)
        if product.quantity > 0:
            product_card.quantity +=1
            product.quantity -=1
            product_card.save()
            product.save()
        else:
            pass
            # masulot yetarlik emas
    return redirect('my_cart')

def decrease_product(request):
    product_id = request.POST['product_id']
    card_id = request.POST['card_id']
    card = Card.objects.get(id=card_id)
    product = Product.objects.get(id=product_id)
    product_card = ProductCard.objects.get(card=card, product=product)
    if product_card.quantity == 1:
        product_card.delete()
    elif product_card.quantity > 1:
        product_card.quantity -=1
        product_card.save()
    product.quantity +=1
    product.save()
    return redirect('my_cart')


def delete_product_from_card(request):
    product_id = request.POST['product_id']
    card_id = request.POST['card_id']
    card = Card.objects.get(id=card_id)
    product = Product.objects.get(id=product_id)
    product_card = ProductCard.objects.get(card=card, product=product)
    product.quantity += product_card.quantity
    product.save()
    product_card.delete()
    return redirect('my_cart')
    