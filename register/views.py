from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from main.models import UserModel
def sign_up(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        re_password = request.POST['re_pass']
        img = request.FILES['img']
        if password==re_password:
            try:
                UserModel.objects.create_user(
                    username=name,
                    email=email,
                    password=password,
                    img=img
                    )
                return redirect('sign_in')
            except:
                messages.error(request,'Username already registred')
               
        else:
            messages.error(request,'Password confrimation error')
    return render(request,'authentication/sign_up.html')

def sign_in(request):
    if request.method == 'POST':
        name = request.POST['your_name']
        password = request.POST['your_pass']
        user = authenticate(username=name,password=password)
        if user is not None:
            login(request,user)
            return redirect('home_page')
        else:
            messages.error(request,'Username or password incorrect')
            return redirect('sign_in')
    return render(request,'authentication/sign_in.html')

def log_out(request):
    logout(request)
    return redirect('home_page')