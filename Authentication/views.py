from django.shortcuts import render, redirect
from Authentication.forms import CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from Authentication.models import CustomUser

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        regsiter_form = CustomUserCreationForm(request.POST)
        if regsiter_form.is_valid():
            new_user = regsiter_form.save()
            username = regsiter_form.cleaned_data.get('username')
            messages.success(request, f"Hey {username}, your account was created successfully!")
            new_user = authenticate(username=regsiter_form.cleaned_data.get('username'), 
                                    password=regsiter_form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect('core:index')
    else:
        regsiter_form = CustomUserCreationForm()
    
    context = {
        'form': regsiter_form,
    }
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Already logged in")
        return redirect('core:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(username=username)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in!')
                return redirect('core:index')
            else:
                messages.warning(request, 'User does not exist. Create an account.')
        except:
            messages.warning(request, f"User with username {username} does not exist")

    context = {

    }
    return render(request, "userauths/sign-in.html", context)


def logout_view(request):
    logout(request)
    #messages.success(request, 'You logged Out.')
    return redirect('')