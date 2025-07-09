from django.shortcuts import render,redirect
from users.forms import RegisterForm,LoginForm
from django.contrib.auth import login,authenticate,logout
# Create your views here.


def sign_up(request):
   form = RegisterForm()
   if request.method=='POST':
       form=RegisterForm(request.POST)
       if form.is_valid():
           form.save()
           return redirect('sign-in')
          
   return render(request,'users/register.html',{'form':form})


def sign_in(request):
   form = LoginForm()
   if request.method=='POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       print(username,password)
       user = authenticate(request,username=username,password=password)
       if user is not None:
           login(request,user)
           return redirect('home')
   return render(request,'users/login.html',{'form':form})


def user_logout(request):
   if request.method=='POST':
       logout(request)
       return redirect('sign-in')

