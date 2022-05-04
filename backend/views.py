from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm


# Create your views here.
def base(request):
    return redirect('main')


def main(request):
    if request.user.is_authenticated:
        return render(request, 'main.html', {'auth': True, 'username': request.user.username})
    else:
        return render(request, 'main.html', {'auth': False})


def user_reg(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')

        return render(request, 'reg.html', {'form': form})

    form = UserForm()
    return render(request, 'reg.html', {'form': form})


def user_login(request):
    form = UserForm()

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('main')

        return render(request, 'login.html', {'form': form, 'invalid': True})

    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('main')