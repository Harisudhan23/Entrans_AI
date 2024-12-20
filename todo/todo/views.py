from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from todo import models
from todo.models import TODO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def home(request):
    return render(request, 'sign.html')

def signup(request):
    if request.method=='POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user = User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/login')
    
    return render(request, 'sign.html')

def login(request):
    if request.method=='POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm,pwd)
        userr = authenticate(request, Username = fnm, password = pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/todopage')
        else:
            return redirect('/login')
    return render(request, 'login.html') 

@login_required(login_url='/login')
def todo(request):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj= models.TODO(title=title,user=request.user)
        obj.save()
        user = request.user
        res = models.TODO.objects.filter(user=user).order_by('-date')
        return redirect('/todopage',{'res': res})
    res = models.TODO.objects.filter(user=request.user).order_by('-date')
    return render(request,'todo.html',{'res': res})

@login_required(login_url='/login')
def edit_todo(request, srno):
    if request.method=='POST':
        title=request.POST.get('title')
        print(title)
        obj= models.TODO.objects.get(srno=srno)
        obj.title=title
        obj.save()
        
        return redirect('/todopage',{'obj': obj})
    obj= models.TODO.objects.get(srno=srno)
     
    return render(request,'edit_todo.html')

@login_required(login_url='/login')
def delete_todo(request,srno):
    obj = models.TODO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/login')

    
       