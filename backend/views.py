from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from rest_framework.views import APIView
from rest_framework.response import Response


def base(request):
    return redirect('main')


def main(request):
    return render(request, 'main.html', {'auth': request.user.is_authenticated, 'username': request.user.username})


class RegView(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'reg.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        return render(request, 'reg.html', {'form': form})


class LoginView(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserForm()
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('main')
        return render(request, 'login.html', {'form': form, 'invalid': True})


@login_required
def user_logout(request):
    logout(request)
    return redirect('main')