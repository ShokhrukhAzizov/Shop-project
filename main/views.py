from django.shortcuts import render
from .models import Category

def index_page(request):
    category = Category.objects.all()
    context = {
        'category':category
    }
    return render(request,'index.html',context)
