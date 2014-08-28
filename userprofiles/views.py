#-*- coding: utf-8 -*-

from django.shortcuts import redirect, render_to_response
from products.models import Rubric
from pages.views import get_context
from django.contrib.auth import authenticate
from aksvrnru.views import error
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from userprofiles.models import *

def login_page(request):
    if request.user.is_authenticated() :
        return error(request, "Ошибка", "Пользователь авторизован как %s." % str(request.user.username))
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response("pages/login_page.html", c)

def login_proc(request):
    user = authenticate(username=request.POST.get("username"), password=request.POST.get("passwd"))
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(reverse('me'))
        else:
            return error(request, "Ошибка авторизации", "Учетная запись не активна.")
    else:
        return error(request, "Ошибка авторизации", "Неверные логин или пароль.")

def me(request):
    if request.user.is_authenticated() :
        return render_to_response("pages/me.html", get_context(request))
    else:
        return redirect(reverse('login_page'))

def logout_view(request):
    logout(request)
    return redirect(reverse('home'))

def signup_view(request):
    if request.user.is_authenticated() :
        return redirect(reverse('me'))
    else:
        c = {}
        c.update(csrf(request))

        return render_to_response("pages/signup.html", c)

def signup(request):
    if request.user.is_authenticated() :
        return redirect(reverse('me'))
    else:
        username = request.POST.get("username")
        try:
            User.objects.get(username=username)
            return error(request, "Ошибка", "Имя пользователя %s занято." % str(username))
        except User.DoesNotExist :
            pass
        email = request.POST.get("email")
        try:
            User.objects.get(email=email)
            return error(request, "Ошибка", "Email %s занят." % str(email))
        except User.DoesNotExist :
            pass
        user = User.objects.create_user(username, email, request.POST.get("passwd"))
        user.first_name = request.POST.get("first_name")
        user.second_name = request.POST.get("second_name")
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.phone = request.POST.get("phone")
        user_profile.save()
        return login_proc(request)
