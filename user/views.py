from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from base.models import Customer

# Create your views here.


def register_user(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            customer = Customer.objects.create(user=user,name = user.username,email=user.email)
            customer.save()
            login(request,user)
            return redirect('base:home_page')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'form': form}
    return render(request,'user/login_register.html',context)

def login_user(request):
    page = 'login'
   
    if request.user.is_authenticated:
         if request.user.is_superuser:
            return redirect('dashboard:index')
         return redirect('base:home_page')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            # check have user or not
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exits')

        # check username nad password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:home_page')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'user/login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('base:home_page')