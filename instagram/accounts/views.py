from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
    PasswordChangeForm
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('feeds:index')

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('feeds:index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form 
    }
    return render(request, 'accounts/login.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('feeds:index')

    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User()
        user.email = email
        user.first_name = first_name
        user.username = username
        user.password = password
        user.save()
        auth_login(request, user)
        return redirect('feeds:index')

        # if form.is_valid():            
        #     user = form.save()
        #     auth_login(request, user)
        #     return redirect('feeds:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def logout(request):
    if request.method=="POST":
        auth_logout(request)
    return redirect('accounts:login')


@login_required
def edit(request):
    if request.method=="POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('feeds:index')
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/edit.html', context)


@login_required
def password(request):
    if request.method=="POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('feeds:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/chg_pw.html', context)