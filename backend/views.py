from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import UserForm
from .models import Core, StrBoost, IntBoost
from .serializers import CoreSerializer


def base(request):
    return redirect('main')


def main(request):
    if request.user.is_authenticated:
        core = Core.objects.get(user=request.user)
    else:
        core = Core()
    return render(request, 'main.html', {'auth': request.user.is_authenticated, 'core': core})


class RegView(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'reg.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            str_boost = StrBoost()
            str_boost.save()
            int_boost = IntBoost()
            int_boost.save()
            core = Core(user=user, str_boost=str_boost, int_boost=int_boost)
            core.save()
            return redirect('main')
        return render(request, 'reg.html', {'form': form})


class LoginView(APIView):
    form = UserForm()

    def get(self, request):
        return render(request, 'login.html', {'form': self.form})

    def post(self, request):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('main')
        return render(request, 'login.html', {'form': self.form, 'invalid': True})


@login_required
def user_logout(request):
    logout(request)
    return redirect('main')


@api_view(['GET'])
@login_required
def call_click(request):
    core = Core.objects.get(user=request.user)
    core.click()
    core.save()

    return Response({'core': CoreSerializer(core).data})


@api_view(['GET'])
@login_required
def str_upgrade(request):
    core = Core.objects.get(user=request.user)
    core.str_upgrade()
    core.save()

    return Response({'core': CoreSerializer(core).data})

@api_view(['GET'])
@login_required
def int_upgrade(request):
    core = Core.objects.get(user=request.user)
    core.int_upgrade()
    core.save()

    return Response({'core': CoreSerializer(core).data})